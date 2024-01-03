import boto3
import json
import re

def get_bedrock_client():
    # Bedrock client used to interact with APIs around models
    bedrock = boto3.client('bedrock', region_name='us-east-1')
    # Bedrock Runtime client used to invoke and question the models
    bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

    return bedrock, bedrock_runtime

def load_prompts_file(file_name = "prompts.json"):
    file = open(file_name)
    data_json = json.load(file)

    return data_json

def get_prompt(*prompt_args):
    prompts = load_prompts_file()    
    prompt_initial = prompts[prompt_args[0]]["prompt"][0]
    prompt_properties_tuple = prompt_args[1:]
    prompt_final = prompt_initial.format(*prompt_properties_tuple)  

    return prompt_final

def bedrock_response(bedrock_runtime, prompt):
    # The payload to be provided to Bedrock
    prompt_body = json.dumps(
        {
            "prompt": "Human:"+ prompt +"\nAssistant:",
            "max_tokens_to_sample": 1500,
            "stop_sequences": [  "\n\nHuman:"   ],
        }
    )

    # The actual call to retrieve an answer from the model
    response = bedrock_runtime.invoke_model(
        body=prompt_body,
        modelId="anthropic.claude-v2",
        accept='application/json',
        contentType='application/json'
    )

    return json.loads(response.get('body').read())

def extract_data(raw_answer):

    # Extract json formated data from Bedrock's raw answer
    FINAL_RESPONSE_REGEX = r"<response>([^<]+)</response>"
    FINAL_RESPONSE_PATTERN = re.compile(FINAL_RESPONSE_REGEX, re.DOTALL)

    #Extract json from the answer
    matched_answer = FINAL_RESPONSE_PATTERN.search(raw_answer)
    matched_answer_json = json.loads(matched_answer.group(1).strip())
    if not matched_answer_json:
        raise Exception("Could not parse raw LLM output")
        
    return matched_answer_json

def get_sites(locations):
    sites = []

    for location_json in locations:
        if location_json["main"] or location_json["tpartner"]:
            continue
        else:
            sites.append(location_json)

    return sites

def lambda_handler(event, context):
    industry = event["industry"]
    country = event["country"]
    date_time = event["datetime"]

    _, bedrock_runtime = get_bedrock_client()

    # Bedrock prompts 
    product_prompt = get_prompt("products", industry, country)
    products_raw_answer = bedrock_response(bedrock_runtime, product_prompt)["completion"]
    products_matched_answer = extract_data(products_raw_answer)
    
    locations_prompt = get_prompt("locations", industry, country)
    locations_raw_answer = bedrock_response(bedrock_runtime, locations_prompt)["completion"]
    locations_matched_answer = extract_data(locations_raw_answer)

    sites = get_sites(locations_matched_answer)
    sites_ids_str = ", ".join([site["id"] for site in sites]) 
    
    for product_json in products_matched_answer:
        product_price = product_json["price"]
        currency = product_json["currency"]
        product_name = product_json["name"]
        product_uom = product_json["unit"]

        product_policy_prompt = get_prompt("policies", industry, country,product_name, product_price, currency, sites_ids_str, product_uom)

        policy_raw_answer = bedrock_response(bedrock_runtime, product_policy_prompt)["completion"]
        print(policy_raw_answer)
        policy_matched_answer = extract_data(policy_raw_answer)
        product_json["policies"] = policy_matched_answer
        
    resp = {
        "country" : country,
        "industry": industry,
        "products": products_matched_answer,
        "locations": locations_matched_answer,
        "datetime": date_time

    }
    
    return {
        'statusCode': 200,
        'body': (resp)
    }


# if __name__ == "__main__":
#     raw_answer = '''<response>[{"address":"Calle Miraflores 1234","city":"Santiago","id":"ABC12345","latitude":"-33.456789","longitude":"-70.123456","time_zone":"America/Santiago","postal_code":"123456","phone_number":"5612345678","country_code":"CL","state_prov":"Región Metropolitana","main":true,"tpartner":false},{"address":"Avenida Providencia 5678","city":"Providencia","id":"XYZ67890","latitude":"-33.456789","longitude":"-70.654321","time_zone":"America/Santiago","postal_code":"765432","phone_number":"5698765432","country_code":"CL","state_prov":"Región Metropolitana","main":false,"tpartner":true},{"address":"Pasaje Los Alamos 987","city":"Viña del Mar","id":"QWE12345","latitude":"-33.000000","longitude":"-71.000000","time_zone":"America/Santiago","postal_code":"123456","phone_number":"5612345678","country_code":"CL","state_prov":"Región de Valparaíso","main":false,"tpartner":false},{"address":"Calle Valdivia 1357","city":"Valdivia","id":"ZXC09876","latitude":"-39.800000","longitude":"-73.200000","time_zone":"America/Santiago","postal_code":"145000","phone_number":"5632198765","country_code":"CL","state_prov":"Región de Los Ríos","main":false,"tpartner":false},{"address":"Calle O'Higgins 456","city":"Rancagua","id":"REW23456","latitude":"-34.166667","longitude":"-70.716667","time_zone":"America/Santiago","postal_code":"623000","phone_number":"5632198765","country_code":"CL","state_prov":"Región de O'Higgins","main":false,"tpartner":false},{"address":"Calle Bilbao 789","city":"Concepción","id":"TYU34567","latitude":"-36.833333","longitude":"-73.050000","time_zone":"America/Santiago","postal_code":"4087000","phone_number":"5641123456","country_code":"CL","state_prov":"Región del Bío Bío","main":false,"tpartner":false},{"address":"Calle Prat 1011","city":"Puerto Montt","id":"IOP45678","latitude":"-41.468333","longitude":"-72.950000","time_zone":"America/Santiago","postal_code":"5120000","phone_number":"5651234567","country_code":"CL","state_prov":"Región de Los Lagos","main":false,"tpartner":false},{"address":"Calle Chacabuco 1213","city":"Coyhaique","id":"ASD56789","latitude":"-45.566667","longitude":"-72.066667","time_zone":"America/Santiago","postal_code":"5770000","phone_number":"5664123456","country_code":"CL","state_prov":"Región de Aysén","main":false,"tpartner":false}]</response>'''
#     matched_answer = extract_data(raw_answer)

#     print(json.dumps(matched_answer, indent=2))