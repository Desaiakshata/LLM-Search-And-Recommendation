from typing import Union
import pandas as pd 
import numpy as np
from fastapi import FastAPI
import openai
import json
from openai.embeddings_utils import cosine_similarity
from fastapi.middleware.cors import CORSMiddleware

openai.api_key = "insert-key-here"
f = open('proddata.json','r')
data = json.load(f)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/search")
def product_search(text: Union[str, None]=None):
    searchres = []
    res = {}
    print("text:",text)
    print("SearchStart...")
    text_emb = get_embedding(text)
    similarities = {}
    for i,d in enumerate(data.items()):
        k,v=d
        # v = v[0]
        similarities[k] = cosine_similarity(v[0], text_emb)
    ss = {k: v for k, v in sorted(similarities.items(), key=lambda item: item[1], reverse=True)}
    for asin in list(ss.keys())[:10]:
        res = {}
        res["pid"] = asin
        res["pname"] = data[asin][1]
        res["purl"] = f"https://rthn.s3.us-east-2.amazonaws.com/im/{asin}.png"
        searchres.append(res)
    print("SearchDone!!")
    # print(searchres)
    return searchres
    #return [{'pid': 'B00MY5OB9K', 'pname': 'essie Nail Color Polish', 'purl': 'https://rthn.s3.us-east-2.amazonaws.com/im/B00MY5OB9K.png'}, {'pid': 'B00MY5OB9K', 'pname': 'essie Nail Color Polish', 'purl': 'https://rthn.s3.us-east-2.amazonaws.com/im/B00MY5OB9K.png'}, {'pid': 'B00MY5OB9K', 'pname': 'essie Nail Color Polish', 'purl': 'https://rthn.s3.us-east-2.amazonaws.com/im/B00MY5OB9K.png'}, {'pid': 'B00MY5OB9K', 'pname': 'essie Nail Color Polish', 'purl': 'https://rthn.s3.us-east-2.amazonaws.com/im/B00MY5OB9K.png'}, {'pid': 'B00MY5OB9K', 'pname': 'essie Nail Color Polish', 'purl': 'https://rthn.s3.us-east-2.amazonaws.com/im/B00MY5OB9K.png'}, {'pid': 'B00MY5OB9K', 'pname': 'essie Nail Color Polish', 'purl': 'https://rthn.s3.us-east-2.amazonaws.com/im/B00MY5OB9K.png'}, {'pid': 'B00MY5OB9K', 'pname': 'essie Nail Color Polish', 'purl': 'https://rthn.s3.us-east-2.amazonaws.com/im/B00MY5OB9K.png'}, {'pid': 'B00MY5OB9K', 'pname': 'essie Nail Color Polish', 'purl': 'https://rthn.s3.us-east-2.amazonaws.com/im/B00MY5OB9K.png'}, {'pid': 'B00MY5OB9K', 'pname': 'essie Nail Color Polish', 'purl': 'https://rthn.s3.us-east-2.amazonaws.com/im/B00MY5OB9K.png'}, {'pid': 'B00MY5OB9K', 'pname': 'essie Nail Color Polish', 'purl': 'https://rthn.s3.us-east-2.amazonaws.com/im/B00MY5OB9K.png'}]


@app.get("/recommend")
def product_recommend():
    prddata = []
    prdres1 = []
    prdres2 = []
    prdres3 = []
    print("starting1")
    rec1_items = recommend1()
    for k,v in rec1_items.items():
        prdres1.append({"pid":k,"pname":v,"purl":f"https://rthn.s3.us-east-2.amazonaws.com/im/{k}.png"})
    print("starting2")
    rec2_items = recommend2()
    for k,v in rec2_items.items():
        prdres2.append({"pid":k,"pname":v,"purl":f"https://rthn.s3.us-east-2.amazonaws.com/im/{k}.png"})
    print("starting3")
    rec3_items = recommend3()
    for k,v in rec3_items.items():
        prdres3.append({"pid":k,"pname":v,"purl":f"https://rthn.s3.us-east-2.amazonaws.com/im/{k}.png"})
    print("done!!")
    # print(prdres)
    prddata.extend([prdres1,prdres2,prdres3])
    return prddata #[{"rec1": rec1_items, "rec2": rec2_items, "rec3": rec3_items}]

@app.get("/clicked")
def clicked(id: Union[str, None]=None):
    # with open('product_id.txt', 'w'):
    #     f.write(id)
    return True


def get_embedding(text, model="text-embedding-ada-002"):
   # text = text[0].replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

def recommend1(products=None, userproducts=None):
    # Given similar users and their product candidate list, 
    # rank the candidate products to suggest to the user
    products = ["B00005JS5C", "B001E96LUO", "B001ET7FZE", "B001F51RAG", "B001F51RAG", "B002GP80EU", "B0046XQ75Y", "B005IHT94S", "B00C92OA30", "B00EYZY6LQ", "B00KIYTQ8U", "B00W259T7G", "B00W259T7G", "B00W259T7G", "B01BNEYGQU", "B00027C9AU", "B001O8KKW0", "B00HADEHUO", "B00IA6KJF2", "B010C79X8K", "1620213982", "B000NKJIXM", "B0010ZBORW", "B0010ZBORW", "B001ET7FZE", "B00CZH3K1C", "B00DY59MB6", "B00DY59MB6", "B00EYZY6LQ", "B00W259T7G", "B013G464EM", "B016V8YWBC", "B01BNEYGQU", "B01CHS3CHA", "B01G08QMAW", "B00CZH3LQG", "B00N2WQ2IW", "B011ABK2LO"]
    userproducts = ["B00005JS5C", "B001E96LUO", "B001ET7FZE", "B001F51RAG", "B001F51RAG", "B002GP80EU", "B0046XQ75Y", "B005IHT94S", "B00C92OA30", "B00EYZY6LQ", "B00KIYTQ8U", "B00W259T7G", "B00W259T7G", "B00W259T7G", "B01BNEYGQU", "B00027C9AU", "B001O8KKW0", "B00HADEHUO", "B00IA6KJF2", "B010C79X8K"]
    return {'B001E96LUO': 'Clean & Clear Deep Action Cream Facial Cleanser for Sensitive Skin, Gentle Daily Face Wash with Oil-Free, 6.5 oz (Pack of 4)',
    'B00DY59MB6': 'Crest Pro-Health For Life CPC Antigingivitis/Antiplaque Smooth Mint Rinse 33.8 Fl Oz',
    'B0010ZBORW': 'Urban Spa Moisturizing Booties to Keep your Feet Smooth, Hydrated and Moisturized',
    'B000NKJIXM': 'Crest Pro-health Multi-Protection Rinse, Cool Wintergreen, 33.8 Fluid Ounce',
    'B001F51RAG': 'Oral-B Glide Pro-Health Dental Floss, Original Floss, 50m, Pack of 6',
    'B001ET7FZE': ' Colgate Fluoride Toothpaste Strawberry Smash Liquid Gel 4.60 oz (Pack of 6) ',
    'B00CZH3K1C': 'Crest + Oral-B Professional Gingivitis Kit, 1 Count'}

def recommend2():
    # Based on the recently bought product recommend 
    # contextually relevant products
    # f = open('product_id.txt','r')
    # product_id = f.read()
    # completion = openai.ChatCompletion.create(
    #   model="gpt-3.5-turbo",
    #   messages=[
    #     {"role": "system", "content": f"You will be provided a product name. Recommend 8 products that a user would buy next. Format the output as a json list. Do not include any additional information in your response and just output the list with product names."},
    #     {"role": "user", "content": f"Product: Colgate Fluoride Toothpaste Strawberry Smash Liquid Gel 4.60 oz (Pack of 6)"} #{data[product_id][1]}"}
    #   ]
    # )
    # res = {}
    # prd_list = json.loads(completion.choices[0].message["content"])
    # for prd in prd_list:
    #     text_emb = get_embedding(prd)
    #     maxsim = 0
    #     prd_name = ''
    #     prd_id = ''
    #     for i,d in enumerate(data.items()):
    #         k,v=d
    #         sim = cosine_similarity(v[0], text_emb)
    #         if maxsim<sim:
    #             maxsim = sim
    #             prd_name = v[1]
    #             prd_id = k
    #     res[prd_id] = prd_name
    # print(res)
    return {'B00KB6Q520': 'Crest Pro-Health Toothpaste, Fluoride, Clinical Gum Protection, Clean Mint, 4 oz (6 Pack)', 'B01E00LEJ6': 'Oral-B Pro 3000 Electronic Power Rechargeable Battery Electric Toothbrush &amp; Oral-B 3D White Replacement Electric Toothbrush Head 3 Count Bundle', 'B00K35EEE0': 'Listerine Total Care Plus Whitening Anticavity Mouthwash, Fresh Mint 16 oz (Pack of 2)', 'B00UJEUY1M': 'GUM&reg; Soft-Picks&reg;, 120 CT (6 PACK)', 'B00INWYJ90': 'Sensodyne Pronamel Fluoride Rinse Mouthwash, 15.5 Ounce', 'B00TV5GSM4': 'Waterpik WP-114W Ultra Designer Black Countertop Water Flosser', 'B00V7B1C62': 'Mouth Kote Dry Mouth Spray, Oral Moisturizer with Yerba Santa, 8 Fluid Ounce (PACK OF 2)', 'B003UNLD96': 'Philips HX5351 Sonicare Toothbrush'}
    # 'B00CZH3K1C': 'Crest + Oral-B Professional Gingivitis Kit, 1 Count'}
    # return res


def recommend3():
    # Based on the current trend, 
    # recommend products to the user
    # completion = openai.ChatCompletion.create(
    #   model="gpt-3.5-turbo",
    #   messages=[
    #     {"role": "system", "content": f"Recommend 5 trending beauty and personal care products. Format the output as a json list. Format the output as a json list. Do not include any additional information in your response and just output the list with product names."},
    #   ]
    # )
    # prd_list = json.loads(completion.choices[0].message["content"])
    # print(prd_list)
    # res = {}
    # for prd in prd_list:
    #     text_emb = get_embedding(prd)
    #     maxsim = 0
    #     prd_name = ''
    #     prd_id = ''
    #     for i,d in enumerate(data.items()):
    #         k,v=d
    #         sim = cosine_similarity(v[0], text_emb)
    #         if maxsim<sim:
    #             maxsim = sim
    #             prd_name = v[1]
    #             prd_id = k
    #     print(prd_id, prd_name)
    #     res[prd_id] = prd_name
    res = {
        "B01H65WJ3W": "Passport To Beauty Gypsetter Luminous Lips Lip Gloss, Bohemian Glow",
        "B003XSINE6": "Be Natural Organics Niacin Complex Balancing Mist 2 Oz (60 ml)",
        "B01AKTL2U2": "Collagen Lip Plumping Mask",
        "B00UQYDSNQ": "Gosh Eye Brow Pencil",
        # "B01B9OEDKS": "Drunk Elephant B-Hydra Intensive Hydration Serum - Gluten Free Anti Wrinkle Serum for All Skin Types (50 ml / 1.69 fl oz)"
      }
    return res



def chat_completion():

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You will be given a product title. You have to find the product name. Give a 1 word product category"},
        {"role": "user", "content": ' '.join(df2['title'][32890])}
      ]
    )
    return completion.choices[0].message