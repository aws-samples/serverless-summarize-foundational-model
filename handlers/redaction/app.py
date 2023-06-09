import json

def lambda_handler(event, context):
    print(json.dumps(event))

    input_text = event['text']
    pii_entities = event['piiEntities']
    comprehend_txt = event['text']

    # reversed to not modify the offsets of other entities when substituting
    print("Detected Entities: ")
    for entity in reversed(pii_entities['entities']):
        comprehend_txt = input_text[:entity['BeginOffset']] + entity['Type'] + comprehend_txt[entity['EndOffset']:]
    
    print(comprehend_txt)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "response": comprehend_txt,
        }).encode('utf-8'),
    }