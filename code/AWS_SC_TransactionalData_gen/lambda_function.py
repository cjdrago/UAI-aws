import os
from Forecast.generator import gen_forecast
from Inbound.generators import gen_inbound_order, gen_inbound_order_line, gen_inbound_order_schedule
from Inventory.generator import gen_inventory
from Outbound.generator import gen_outbound_order_line, gen_outbound_shipment
from Shipment.generator import gen_shipment
from dates import  get_today_date
from helpers import create_transactional_folder, get_params, get_variable_name, load_data, save_as_csv
import boto3
import json
from io import StringIO


s3 = boto3.client('s3')
sts = boto3.client('sts')

def csv_into_s3(partitions, data_df, file_name, bucket = "aws-sc-data"):
    AWS_ACCOUNT_ID = sts.get_caller_identity()["Account"]

    csv_buffer = StringIO()
    data_df.to_csv(csv_buffer)
    s3.put_object(
        Bucket = bucket+'-'+ AWS_ACCOUNT_ID,
        Key = partitions + file_name,
        Body = csv_buffer.getvalue()
    )

def inbound_order(params, t_date, partition, num_periods = 65):
    InboundOrderLine_Records = gen_inbound_order_line(params, t_date, num_periods)
    InboundOrderLineSchedule_Records = gen_inbound_order_schedule(InboundOrderLine_Records.copy())
    InboundOrder_Records = gen_inbound_order(InboundOrderLine_Records.copy())

    csv_into_s3(partition, InboundOrderLine_Records, get_variable_name(InboundOrderLine_Records=InboundOrderLine_Records)+'.csv')
    csv_into_s3(partition, InboundOrderLineSchedule_Records, get_variable_name(InboundOrderLineSchedule_Records=InboundOrderLineSchedule_Records)+'.csv')
    csv_into_s3(partition, InboundOrder_Records, get_variable_name(InboundOrder_Records=InboundOrder_Records)+'.csv')
    # save_as_csv(InboundOrderLine_Records, get_variable_name(InboundOrderLine_Records=InboundOrderLine_Records))
    # save_as_csv(InboundOrderLineSchedule_Records, get_variable_name(InboundOrderLineSchedule_Records=InboundOrderLineSchedule_Records))
    # save_as_csv(InboundOrder_Records, get_variable_name(InboundOrder_Records=InboundOrder_Records))

    return InboundOrderLine_Records, InboundOrderLineSchedule_Records

def forecast(params, t_date, partition):

    Forecast_Records = gen_forecast(params, t_date)

    csv_into_s3(partition, Forecast_Records, get_variable_name(Forecast_Records=Forecast_Records)+'.csv')
    # save_as_csv(Forecast_Records, get_variable_name(Forecast_Records=Forecast_Records))
 
def shipment(params, InboundOrderLineSchedule_Records_copy, InboundOrderLine_Records_copy, partition):
    Shipment_Records = gen_shipment(InboundOrderLineSchedule_Records_copy, InboundOrderLine_Records_copy, params)

    csv_into_s3(partition, Shipment_Records, get_variable_name(Shipment_Records=Shipment_Records)+'.csv')
    # save_as_csv(Shipment_Records, get_variable_name(Shipment_Records=Shipment_Records))
   
def inventory(params, t_date, partition):
    InventoryLevel_Records = gen_inventory(params, t_date)

    csv_into_s3(partition, InventoryLevel_Records, get_variable_name(InventoryLevel_Records=InventoryLevel_Records)+'.csv')
    # save_as_csv(InventoryLevel_Records, get_variable_name(InventoryLevel_Records=InventoryLevel_Records))

def outbound_order(params, t_date, partition):
    OutboundOrderLine_Records = gen_outbound_order_line(params, t_date)
    OutboundShipment_Records = gen_outbound_shipment(OutboundOrderLine_Records.copy())

    csv_into_s3(partition, OutboundOrderLine_Records, get_variable_name(OutboundOrderLine_Records=OutboundOrderLine_Records)+'.csv')
    csv_into_s3(partition, OutboundShipment_Records, get_variable_name(OutboundShipment_Records=OutboundShipment_Records)+'.csv')
    # save_as_csv(OutboundOrderLine_Records, get_variable_name(OutboundOrderLine_Records=OutboundOrderLine_Records))
    # save_as_csv(OutboundShipment_Records, get_variable_name(OutboundShipment_Records=OutboundShipment_Records))

def lambda_handler(event, context):
    
    date_time = str(event['body']['datetime'])
    country = event['body']['country']
    industry = event['body']['industry']
    sites_ids = event["body"]["sites"]
    products_ids = event["body"]["products"]

    params = get_params(sites_ids, products_ids)
    base_path = os.getcwd()
    create_transactional_folder(base_path)
    
    t_date = get_today_date()
    partitions =  'country='+country + '/industry=' + industry + '/' + date_time +'/' 

    InboundOrderLine_Records, InboundOrderLineSchedule_Records = inbound_order(params, t_date, partitions)
    forecast(params, t_date, partitions)
    shipment(params, InboundOrderLineSchedule_Records.copy(), InboundOrderLine_Records.copy(), partitions)
    inventory(params, t_date, partitions)
    outbound_order(params, t_date, partitions)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Data generated!', ' partition':partitions})
    }

if __name__ == "__main__":
    event = load_data()
    lambda_handler(event, "")