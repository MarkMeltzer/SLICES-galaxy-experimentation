import json, requests,sys

src_lang = sys.argv[1]
tgt_lang = sys.argv[2]
input_json = json.loads(sys.stdin.read())

output_json = []
for item in input_json:
    output_json.append(requests.request(
        url=f"https://lindat.mff.cuni.cz/services/translation/api/v2/languages/?src={src_lang}&tgt={tgt_lang}",
        method="POST",
        headers={
            "accept": "application/json",
            "Content-Type" : "application/x-www-form-urlencoded"
        },
        data=f"input_text={item}"
    ).json()[0].strip())

print(json.dumps(output_json, indent=4))