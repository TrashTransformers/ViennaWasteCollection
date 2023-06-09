import os
from classifiers.clip import classify_with_clip

from classifiers.classification_common import (
    folders_with_category,
    file_paths_override,
)
from torch_tuned import classify_with_resnet


class Mistake:
    def __init__(
        self, image_path: str, category: str, classification: str, probability: float
    ):
        self.image_path = image_path
        self.category = category
        self.classification = classification
        self.probability = probability


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

    def mistake(self, category, classification, image_path, prob):
        mistake = Mistake(image_path, category, classification, prob)
        self.mistakes.append(mistake)
        print_mistakes([mistake])

    def get_accuracy(self):
        if self.count == 0:
            return 0
        return self.success_count / self.count

    def print_mistakes_for_category_mismatch(self, cat_1: str, cat_2: str):
        print(f"Misclassified between {cat_1} and {cat_2}")
        mistakes = []
        for mistake in self.mistakes:
            if mistake.category == cat_1 and mistake.classification == cat_2:
                mistakes.append(mistake)
        print_mistakes_as_python_list(mistakes)


def print_mistakes_as_python_list(mistakes):
    print("[")
    for mistake in mistakes:
        path = mistake.image_path.replace("/", "//")
        print(f"'{path}',")
    print("]")


def print_mistakes(mistakes):
    for mistake in mistakes:
        print(
            f"Category: {mistake.category}, classification: {mistake.classification}"
            + f" probabilty: {mistake.probability} image: {mistake.image_path}"
        )


class CategoryResult:
    def __init__(self, category_name: str):
        self.category_name = category_name
        self.success_count = 0
        self.count = 0


def performance_evaluation_full():
    performance_evaluation(10000, classify_with_clip)


def performance_evaluation(
    limit_per_category: int = 10,
    classification_function=classify_with_clip,
    file_paths_override=None,
    categories_override=None,
):
    images_folder = "../images/"
    categories_to_use = folders_with_category
    if categories_override is not None:
        categories_to_use = categories_override
    result = PerformanceResult(set(categories_to_use.values()))
    limit = 0
    for folder, category in categories_to_use.items():
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
            classification_result = classification_function(image_file)
            classification_category = classification_result.category
            result.image_with_category_processed(category)
            if classification_category == category or mapped_category_matches(
                classification_category, category
            ):
                result.successfull_classification(category)
            else:
                result.mistake(
                    category,
                    classification_category,
                    image_file,
                    classification_result.probability,
                )
            print(
                f"Current accuracy: {result.get_accuracy()*100:.2f}%. Count: {result.count}"
            )

    print_mistakes(result.mistakes)
    print_mistakes_as_python_list(result.mistakes)
    print(f"Accuracy: {result.get_accuracy()*100:.2f}%")
    result.print_mistakes_for_category_mismatch("glass", "metal")
    return result


def mapped_category_matches(classification_category, category):
    if "glass" in category:
        return classification_category == "glass"

    if category == "cardboard":
        return classification_category == "paper"
    return False


def get_all_files_in_folder(folder_path: str):
    file_names = os.listdir(folder_path)
    file_paths = [os.path.abspath(folder_path + "/" + name) for name in file_names]
    return file_paths


test_resnet = True

if test_resnet:
    performance_evaluation(
        limit_per_category=5000,
        classification_function=classify_with_resnet,
        categories_override={
            "brown-glass": "glass",
            "white-glass": "glass",
            "paper": "paper",
            "plastic": "plastic",
            "metal": "metal",
        },
    )
else:
    performance_evaluation(
        limit_per_category=5000,
        classification_function=classify_with_clip,
        file_paths_override=file_paths_override,
    )
