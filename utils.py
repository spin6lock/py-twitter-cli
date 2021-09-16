def gen_image_id(tweet):
    return f"{tweet.user.screen_name}_{tweet.id_str}"

def is_contains_multiple_media(tweet):
    if tweet.extended_entities and tweet.extended_entities.media:
        medias = tweet.extended_entities.media
        return len(medias) > 1
    return False

