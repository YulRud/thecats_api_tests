from util.string_utils import generate_random_string

def get_favorite_body(image_id, sub_id):
    body = {}
    body["image_id"] = image_id
    body["sub_id"] = sub_id

    return body

def get_random_favorite_body():

    return get_favorite_body(generate_random_string(), generate_random_string())