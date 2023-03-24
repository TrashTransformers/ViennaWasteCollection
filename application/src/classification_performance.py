import os
from classifiers.clip import classify_with_clip

from classifiers.classification_common import garbage_classes
from classifiers.clip_2 import classify_with_clip_2


class Mistake:
    def __init__(self, image_path: str, category: str, classification: str):
        self.image_path = image_path
        self.category = category
        self.classification = classification


class PerformanceResult:
    def __init__(self, categories):
        self.results = {}
        for category in categories:
            self.results[category] = CategoryResult(category)
        self.mistakes = []
        self.success_count = 0
        self.count = 0

    def image_with_category_processed(self, category: str):
        result = self.results[category]
        result.count += 1
        self.count += 1

    def successfull_classification(self, category: str):
        result = self.results[category]
        result.success_count += 1
        self.success_count += 1

    def mistake(self, category, classification, image_path):
        self.mistakes.append(Mistake(image_path, category, classification))

    def get_accuracy(self):
        if self.count == 0:
            return 0
        return self.success_count / self.count

    def print_mistakes(self):
        for mistake in self.mistakes:
            print(
                f"Category: {mistake.category}, classification: {mistake.classification}, image: {mistake.image_path}"
            )

    def print_mistakes_as_python_list(self):
        print("[")
        for mistake in self.mistakes:
            path = mistake.image_path.replace("/", "//")
            print(f"'{path}',")
        print("]")


class CategoryResult:
    def __init__(self, category_name: str):
        self.category_name = category_name
        self.success_count = 0
        self.count = 0


def performance_evaluation(
    limit_per_category: int = 10,
    classification_function=classify_with_clip,
    file_paths_override=None,
):
    images_folder = "../images/"
    folders_with_category = {
        # "biological": "organic",
        "brown-glass": "glass",
        "cardboard": "paper",
        "green-glass": "glass",
        "white-glass": "glass",
        "metal": "metal",
        "paper": "paper",
        "plastic": "plastic",
        # "trash": "residual waste",
    }

    result = PerformanceResult(garbage_classes)
    limit = 0
    for folder, category in folders_with_category.items():
        sub_folder = images_folder + folder
        image_files = get_all_files_in_folder(sub_folder)

        limit = 0
        for image_file in image_files:
            if file_paths_override is not None:
                if image_file not in file_paths_override:
                    continue
            if limit > limit_per_category:
                break
            limit += 1
            classification_result = classification_function(image_file).category
            result.image_with_category_processed(category)
            if classification_result == category:
                result.successfull_classification(category)
            else:
                result.mistake(category, classification_result, image_file)
                print(
                    f"Mistake: Category: {category}, classification: {classification_result}, image: {image_file}"
                )
            print(
                f"Current accuracy: {result.get_accuracy()*100:.2f}%. Count: {result.count}"
            )

    result.print_mistakes()
    result.print_mistakes_as_python_list()
    print(f"Accuracy: {result.get_accuracy()*100:.2f}%")


def get_all_files_in_folder(folder_path: str):
    file_names = os.listdir(folder_path)
    file_paths = [os.path.abspath(folder_path + "/" + name) for name in file_names]
    return file_paths


performance_evaluation(
    limit_per_category=20,
    classification_function=classify_with_clip_2,
    file_paths_override=[
        "C:\\Projects\\trashy\\ViennaWasteCollection\\images\\brown-glass\\brown-glass101.jpg",
        # "C:\\Projects\\trashy\\ViennaWasteCollection\\images\\cardboard\\cardboard10.jpg",
        # "C:\\Projects\\trashy\\ViennaWasteCollection\\images\\cardboard\\cardboard100.jpg",
        # "C:\\Projects\\trashy\\ViennaWasteCollection\\images\\cardboard\\cardboard102.jpg",
        # "C:\\Projects\\trashy\\ViennaWasteCollection\\images\\green-glass\\green-glass10.jpg",
        # "C:\\Projects\\trashy\\ViennaWasteCollection\\images\\white-glass\\white-glass101.jpg",
        # "C:\\Projects\\trashy\\ViennaWasteCollection\\images\\white-glass\\white-glass103.jpg",
        # "C:\\Projects\\trashy\\ViennaWasteCollection\\images\\metal\\metal102.jpg",
        # "C:\\Projects\\trashy\\ViennaWasteCollection\\images\\metal\\metal103.jpg",
        # "C:\\Projects\\trashy\\ViennaWasteCollection\\images\\paper\\paper1.jpg",
        # "C:\\Projects\\trashy\\ViennaWasteCollection\\images\\paper\\paper100.jpg",
        # "C:\\Projects\\trashy\\ViennaWasteCollection\\images\\plastic\\plastic101.jpg",
        # "C:\\Projects\\trashy\\ViennaWasteCollection\\images\\plastic\\plastic103.jpg",
    ],
)
