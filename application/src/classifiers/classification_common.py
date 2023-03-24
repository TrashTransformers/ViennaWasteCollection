folders_with_category = {
    # "biological": "organic",
    "brown-glass": "brown-glass",
    "white-glass": "white-glass",
    "paper": "paper",
    "plastic": "plastic",
    "metal": "metal",
    #"cardboard": "paper",
    # "green-glass": "colored-glass",
    # "trash": "residual waste",
}
classes_with_category = {
    # "food": "organic",
    "brown-glass": "brown-glass",
    "white-glass": "white-glass",
    "paper": "paper",
    "plastic": "plastic",
    "metal": "metal",
    "colored glass": "white-glass",
    "white glass": "white-glass",
    "broken white glass": "white-glass",
    "jar white glass": "white-glass",
    "aluminum": "metal",
    "steel": "metal",
    "news paper": "paper",
    "aluminum papier ": "metal",
    # "something else": "residual waste",
}

garbage_classes = list(classes_with_category.keys())



basepath = "C:\\Users\\dejanlinkic\\source\\repos\\ML\\ViennaWasteCollection\\images\\"
file_paths_override  = None
#file_paths_override=[basepath +  'white-glass\\white-glass102.jpg']

