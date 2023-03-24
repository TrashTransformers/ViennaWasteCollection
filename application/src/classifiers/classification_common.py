folders_with_category = {
    # "biological": "organic",
    "brown-glass": "brown-glass",
    "white-glass": "white-glass",
    #"cardboard": "paper",
    # "green-glass": "colored-glass",
    "metal": "metal",
    "paper": "paper",
    "plastic": "plastic",
    # "trash": "residual waste",
}
classes_with_category = {
    # "food": "organic",
    "brown-glass": "brown-glass",
    "colored glass": "white-glass",
    "brown-glass": "brown-glass",
    "broken white glass": "white-glass",
    "jar white glass": "white-glass",
    "metal": "metal",
    "aluminum": "metal",
    "steel": "metal",
    "paper": "paper",
    "news paper": "paper",
    "aluminum papier ": "metal",
    # "something else": "residual waste",
    "plastic": "plastic",
}

garbage_classes = list(classes_with_category.keys())



basepath = "C:\\Users\\dejanlinkic\\source\\repos\\ML\\ViennaWasteCollection\\images\\"
file_paths_override  = None
#file_paths_override=[basepath +  'white-glass\\white-glass102.jpg']

