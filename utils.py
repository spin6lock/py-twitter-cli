def gen_image_id(tweet):
    return f"{tweet.user.screen_name}_{tweet.id_str}"
