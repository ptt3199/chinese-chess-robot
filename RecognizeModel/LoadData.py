import os
import random
import shutil
from PIL import Image
from shutil import copyfile

source_path = '.\\ChessChampImages'


def load_data():
    source_path_black_adviser = os.path.join(source_path, 'Black Adviser')
    source_path_black_cannon = os.path.join(source_path, 'Black Cannon')
    source_path_black_chariot = os.path.join(source_path, 'Black Chariot')
    source_path_black_elephant = os.path.join(source_path, 'Black Elephant')
    source_path_black_king = os.path.join(source_path, 'Black King')
    source_path_black_Knight = os.path.join(source_path, 'Black Knight')
    source_path_black_pawn = os.path.join(source_path, 'Black Pawn')
    
    source_path_red_adviser = os.path.join(source_path, 'Red Adviser')
    source_path_red_cannon = os.path.join(source_path, 'Red Cannon')
    source_path_red_chariot = os.path.join(source_path, 'Red Chariot')
    source_path_red_elephant = os.path.join(source_path, 'Red Elephant')
    source_path_red_king = os.path.join(source_path, 'Red King')
    source_path_red_Knight = os.path.join(source_path, 'Red Knight')
    source_path_red_pawn = os.path.join(source_path, 'Red Pawn')

    print(f"There are {len(os.listdir(source_path_black_adviser))} images of Black Adviser.")
    print(f"There are {len(os.listdir(source_path_black_cannon))} images of Black Cannon.")
    print(f"There are {len(os.listdir(source_path_black_chariot))} images of Black Chariot.")
    print(f"There are {len(os.listdir(source_path_black_elephant))} images of Black Elephant.")
    print(f"There are {len(os.listdir(source_path_black_king))} images of Black King.")
    print(f"There are {len(os.listdir(source_path_black_Knight))} images of Black Knight.")
    print(f"There are {len(os.listdir(source_path_black_pawn))} images of Black Pawn.")
    
    print(f"There are {len(os.listdir(source_path_red_adviser))} images of Red Adviser.")
    print(f"There are {len(os.listdir(source_path_red_cannon))} images of Red Cannon.")
    print(f"There are {len(os.listdir(source_path_red_chariot))} images of Red Chariot.")
    print(f"There are {len(os.listdir(source_path_red_elephant))} images of Red Elephant.")
    print(f"There are {len(os.listdir(source_path_red_king))} images of Red King.")
    print(f"There are {len(os.listdir(source_path_red_Knight))} images of Red Knight.")
    print(f"There are {len(os.listdir(source_path_red_pawn))} images of Red Pawn.")

    # Define root directory
    root_dir = '.\\Classify'
    # Empty directory to prevent FileExistsError is the function is run several times
    if os.path.exists(root_dir):
        shutil.rmtree(root_dir)

    def create_train_val_dirs(root_path):
        """
          Creates directories for the train and test sets

          Args:
            root_path (string) - the base directory path to create subdirectories from

          Returns:
            None
        """
        train_dir = os.path.join(root_path, 'Training')
        os.makedirs(train_dir)
        val_dir = os.path.join(root_path, 'Validation')
        os.makedirs(val_dir)
        train_dir_black_adviser = os.path.join(train_dir, 'Black Adviser')
        os.makedirs(train_dir_black_adviser)
        train_dir_black_cannon = os.path.join(train_dir, 'Black Cannon')
        os.makedirs(train_dir_black_cannon)
        train_dir_black_chariot = os.path.join(train_dir, 'Black Chariot')
        os.makedirs(train_dir_black_chariot)
        train_dir_black_elephant = os.path.join(train_dir, 'Black Elephant')
        os.makedirs(train_dir_black_elephant)
        train_dir_black_Knight = os.path.join(train_dir, 'Black Knight')
        os.makedirs(train_dir_black_Knight)
        train_dir_black_king = os.path.join(train_dir, 'Black King')
        os.makedirs(train_dir_black_king)
        train_dir_black_pawn = os.path.join(train_dir, 'Black Pawn')
        os.makedirs(train_dir_black_pawn)
        train_dir_red_adviser = os.path.join(train_dir, 'Red Adviser')
        os.makedirs(train_dir_red_adviser)
        train_dir_red_cannon = os.path.join(train_dir, 'Red Cannon')
        os.makedirs(train_dir_red_cannon)
        train_dir_red_chariot = os.path.join(train_dir, 'Red Chariot')
        os.makedirs(train_dir_red_chariot)
        train_dir_red_elephant = os.path.join(train_dir, 'Red Elephant')
        os.makedirs(train_dir_red_elephant)
        train_dir_red_Knight = os.path.join(train_dir, 'Red Knight')
        os.makedirs(train_dir_red_Knight)
        train_dir_red_king = os.path.join(train_dir, 'Red King')
        os.makedirs(train_dir_red_king)
        train_dir_red_pawn = os.path.join(train_dir, 'Red Pawn')
        os.makedirs(train_dir_red_pawn)

        val_dir_black_adviser = os.path.join(val_dir, 'Black Adviser')
        os.makedirs(val_dir_black_adviser)
        val_dir_black_cannon = os.path.join(val_dir, 'Black Cannon')
        os.makedirs(val_dir_black_cannon)
        val_dir_black_chariot = os.path.join(val_dir, 'Black Chariot')
        os.makedirs(val_dir_black_chariot)
        val_dir_black_elephant = os.path.join(val_dir, 'Black Elephant')
        os.makedirs(val_dir_black_elephant)
        val_dir_black_Knight = os.path.join(val_dir, 'Black Knight')
        os.makedirs(val_dir_black_Knight)
        val_dir_black_king = os.path.join(val_dir, 'Black King')
        os.makedirs(val_dir_black_king)
        val_dir_black_pawn = os.path.join(val_dir, 'Black Pawn')
        os.makedirs(val_dir_black_pawn)
        val_dir_red_adviser = os.path.join(val_dir, 'Red Adviser')
        os.makedirs(val_dir_red_adviser)
        val_dir_red_cannon = os.path.join(val_dir, 'Red Cannon')
        os.makedirs(val_dir_red_cannon)
        val_dir_red_chariot = os.path.join(val_dir, 'Red Chariot')
        os.makedirs(val_dir_red_chariot)
        val_dir_red_elephant = os.path.join(val_dir, 'Red Elephant')
        os.makedirs(val_dir_red_elephant)
        val_dir_red_Knight = os.path.join(val_dir, 'Red Knight')
        os.makedirs(val_dir_red_Knight)
        val_dir_red_king = os.path.join(val_dir, 'Red King')
        os.makedirs(val_dir_red_king)
        val_dir_red_pawn = os.path.join(val_dir, 'Red Pawn')
        os.makedirs(val_dir_red_pawn)

    try:
        create_train_val_dirs(root_path=root_dir)
    except FileExistsError:
        print("You should not be seeing this since the upper directory is removed beforehand")

    # Test your create_train_val_dirs function
    for rootdir, dirs, files in os.walk(root_dir):
        for subdir in dirs:
            print(os.path.join(rootdir, subdir))

    def split_data(SOURCE_DIR, TRAINING_DIR, VALIDATION_DIR, SPLIT_SIZE):
        source_list = random.sample(os.listdir(SOURCE_DIR), len(os.listdir(SOURCE_DIR)))
        count = 0
        target = TRAINING_DIR
        training_size = int(SPLIT_SIZE * len(source_list))
        for item in source_list:
            item_source = os.path.join(SOURCE_DIR, item)
            if os.path.getsize(item_source) != 0:
                count += 1
                if count == training_size:
                    target = VALIDATION_DIR
                copyfile(item_source, os.path.join(target, item))
            else:
                print(f'{item} is zero length, so ignoring.')
                training_size -= 1

    BLACK_ADVISER_SOURCE_DIR = ".\\ChessChampImages\\Black Adviser"
    BLACK_CANNON_SOURCE_DIR = ".\\ChessChampImages\\Black Cannon"
    BLACK_CHARIOT_SOURCE_DIR = ".\\ChessChampImages\\Black Chariot"
    BLACK_ELEPHANT_SOURCE_DIR = ".\\ChessChampImages\\Black Elephant"
    BLACK_Knight_SOURCE_DIR = ".\\ChessChampImages\\Black Knight"
    BLACK_KING_SOURCE_DIR = ".\\ChessChampImages\\Black King"
    BLACK_PAWN_SOURCE_DIR = ".\\ChessChampImages\\Black Pawn"
    RED_ADVISER_SOURCE_DIR = ".\\ChessChampImages\\Red Adviser"
    RED_CANNON_SOURCE_DIR = ".\\ChessChampImages\\Red Cannon"
    RED_CHARIOT_SOURCE_DIR = ".\\ChessChampImages\\Red Chariot"
    RED_ELEPHANT_SOURCE_DIR = ".\\ChessChampImages\\Red Elephant"
    RED_Knight_SOURCE_DIR = ".\\ChessChampImages\\Red Knight"
    RED_KING_SOURCE_DIR = ".\\ChessChampImages\\Red King"
    RED_PAWN_SOURCE_DIR = ".\\ChessChampImages\\Red Pawn"

    TRAINING_DIR = ".\\Classify\\Training\\"
    VALIDATION_DIR = ".\\Classify\\Validation\\"

    TRAINING_BLACK_ADVISER_DIR = os.path.join(TRAINING_DIR, "Black Adviser")
    VALIDATION_BLACK_ADVISER_DIR = os.path.join(VALIDATION_DIR, "Black Adviser")
    TRAINING_BLACK_CANNON_DIR = os.path.join(TRAINING_DIR, "Black Cannon")
    VALIDATION_BLACK_CANNON_DIR = os.path.join(VALIDATION_DIR, "Black Cannon")
    TRAINING_BLACK_CHARIOT_DIR = os.path.join(TRAINING_DIR, "Black Chariot")
    VALIDATION_BLACK_CHARIOT_DIR = os.path.join(VALIDATION_DIR, "Black Chariot")
    TRAINING_BLACK_ELEPHANT_DIR = os.path.join(TRAINING_DIR, "Black Elephant")
    VALIDATION_BLACK_ELEPHANT_DIR = os.path.join(VALIDATION_DIR, "Black Elephant")
    TRAINING_BLACK_Knight_DIR = os.path.join(TRAINING_DIR, "Black Knight")
    VALIDATION_BLACK_Knight_DIR = os.path.join(VALIDATION_DIR, "Black Knight")
    TRAINING_BLACK_KING_DIR = os.path.join(TRAINING_DIR, "Black King")
    VALIDATION_BLACK_KING_DIR = os.path.join(VALIDATION_DIR, "Black King")
    TRAINING_BLACK_PAWN_DIR = os.path.join(TRAINING_DIR, "Black Pawn")
    VALIDATION_BLACK_PAWN_DIR = os.path.join(VALIDATION_DIR, "Black Pawn")

    TRAINING_RED_ADVISER_DIR = os.path.join(TRAINING_DIR, "Red Adviser")
    VALIDATION_RED_ADVISER_DIR = os.path.join(VALIDATION_DIR, "Red Adviser")
    TRAINING_RED_CANNON_DIR = os.path.join(TRAINING_DIR, "Red Cannon")
    VALIDATION_RED_CANNON_DIR = os.path.join(VALIDATION_DIR, "Red Cannon")
    TRAINING_RED_CHARIOT_DIR = os.path.join(TRAINING_DIR, "Red Chariot")
    VALIDATION_RED_CHARIOT_DIR = os.path.join(VALIDATION_DIR, "Red Chariot")
    TRAINING_RED_ELEPHANT_DIR = os.path.join(TRAINING_DIR, "Red Elephant")
    VALIDATION_RED_ELEPHANT_DIR = os.path.join(VALIDATION_DIR, "Red Elephant")
    TRAINING_RED_Knight_DIR = os.path.join(TRAINING_DIR, "Red Knight")
    VALIDATION_RED_Knight_DIR = os.path.join(VALIDATION_DIR, "Red Knight")
    TRAINING_RED_KING_DIR = os.path.join(TRAINING_DIR, "Red King")
    VALIDATION_RED_KING_DIR = os.path.join(VALIDATION_DIR, "Red King")
    TRAINING_RED_PAWN_DIR = os.path.join(TRAINING_DIR, "Red Pawn")
    VALIDATION_RED_PAWN_DIR = os.path.join(VALIDATION_DIR, "Red Pawn")

    # Empty directories in case you run this cell multiple times
    if len(os.listdir(TRAINING_BLACK_ADVISER_DIR)) > 0:
        for file in os.scandir(TRAINING_BLACK_ADVISER_DIR):
            os.remove(file.path)
    if len(os.listdir(VALIDATION_BLACK_ADVISER_DIR)) > 0:
        for file in os.scandir(VALIDATION_BLACK_ADVISER_DIR):
            os.remove(file.path)
    if len(os.listdir(TRAINING_BLACK_CANNON_DIR)) > 0:
        for file in os.scandir(TRAINING_BLACK_CANNON_DIR):
            os.remove(file.path)
    if len(os.listdir(VALIDATION_BLACK_CANNON_DIR)) > 0:
        for file in os.scandir(VALIDATION_BLACK_CANNON_DIR):
            os.remove(file.path)
    if len(os.listdir(TRAINING_BLACK_CHARIOT_DIR)) > 0:
        for file in os.scandir(TRAINING_BLACK_CHARIOT_DIR):
            os.remove(file.path)
    if len(os.listdir(VALIDATION_BLACK_CHARIOT_DIR)) > 0:
        for file in os.scandir(VALIDATION_BLACK_CHARIOT_DIR):
            os.remove(file.path)
    if len(os.listdir(TRAINING_BLACK_ELEPHANT_DIR)) > 0:
        for file in os.scandir(TRAINING_BLACK_ELEPHANT_DIR):
            os.remove(file.path)
    if len(os.listdir(VALIDATION_BLACK_ELEPHANT_DIR)) > 0:
        for file in os.scandir(VALIDATION_BLACK_ELEPHANT_DIR):
            os.remove(file.path)
    if len(os.listdir(TRAINING_BLACK_Knight_DIR)) > 0:
        for file in os.scandir(TRAINING_BLACK_Knight_DIR):
            os.remove(file.path)
    if len(os.listdir(VALIDATION_BLACK_Knight_DIR)) > 0:
        for file in os.scandir(VALIDATION_BLACK_Knight_DIR):
            os.remove(file.path)
    if len(os.listdir(TRAINING_BLACK_KING_DIR)) > 0:
        for file in os.scandir(TRAINING_BLACK_KING_DIR):
            os.remove(file.path)
    if len(os.listdir(VALIDATION_BLACK_KING_DIR)) > 0:
        for file in os.scandir(VALIDATION_BLACK_KING_DIR):
            os.remove(file.path)
    if len(os.listdir(TRAINING_BLACK_PAWN_DIR)) > 0:
        for file in os.scandir(TRAINING_BLACK_PAWN_DIR):
            os.remove(file.path)
    if len(os.listdir(VALIDATION_BLACK_PAWN_DIR)) > 0:
        for file in os.scandir(VALIDATION_BLACK_PAWN_DIR):
            os.remove(file.path)
    if len(os.listdir(TRAINING_RED_ADVISER_DIR)) > 0:
        for file in os.scandir(TRAINING_RED_ADVISER_DIR):
            os.remove(file.path)
    if len(os.listdir(VALIDATION_RED_ADVISER_DIR)) > 0:
        for file in os.scandir(VALIDATION_RED_ADVISER_DIR):
            os.remove(file.path)
    if len(os.listdir(TRAINING_RED_CANNON_DIR)) > 0:
        for file in os.scandir(TRAINING_RED_CANNON_DIR):
            os.remove(file.path)
    if len(os.listdir(VALIDATION_RED_CANNON_DIR)) > 0:
        for file in os.scandir(VALIDATION_RED_CANNON_DIR):
            os.remove(file.path)
    if len(os.listdir(TRAINING_RED_CHARIOT_DIR)) > 0:
        for file in os.scandir(TRAINING_RED_CHARIOT_DIR):
            os.remove(file.path)
    if len(os.listdir(VALIDATION_RED_CHARIOT_DIR)) > 0:
        for file in os.scandir(VALIDATION_RED_CHARIOT_DIR):
            os.remove(file.path)
    if len(os.listdir(TRAINING_RED_ELEPHANT_DIR)) > 0:
        for file in os.scandir(TRAINING_RED_ELEPHANT_DIR):
            os.remove(file.path)
    if len(os.listdir(VALIDATION_RED_ELEPHANT_DIR)) > 0:
        for file in os.scandir(VALIDATION_RED_ELEPHANT_DIR):
            os.remove(file.path)
    if len(os.listdir(TRAINING_RED_Knight_DIR)) > 0:
        for file in os.scandir(TRAINING_RED_Knight_DIR):
            os.remove(file.path)
    if len(os.listdir(VALIDATION_RED_Knight_DIR)) > 0:
        for file in os.scandir(VALIDATION_RED_Knight_DIR):
            os.remove(file.path)
    if len(os.listdir(TRAINING_RED_KING_DIR)) > 0:
        for file in os.scandir(TRAINING_RED_KING_DIR):
            os.remove(file.path)
    if len(os.listdir(VALIDATION_RED_KING_DIR)) > 0:
        for file in os.scandir(VALIDATION_RED_KING_DIR):
            os.remove(file.path)
    if len(os.listdir(TRAINING_RED_PAWN_DIR)) > 0:
        for file in os.scandir(TRAINING_RED_PAWN_DIR):
            os.remove(file.path)
    if len(os.listdir(VALIDATION_RED_PAWN_DIR)) > 0:
        for file in os.scandir(VALIDATION_RED_PAWN_DIR):
            os.remove(file.path)
    # Define proportion of images used for training
    split_size = .8
    split_data(BLACK_ADVISER_SOURCE_DIR, TRAINING_BLACK_ADVISER_DIR, VALIDATION_BLACK_ADVISER_DIR, split_size)
    split_data(BLACK_CANNON_SOURCE_DIR, TRAINING_BLACK_CANNON_DIR, VALIDATION_BLACK_CANNON_DIR, split_size)
    split_data(BLACK_CHARIOT_SOURCE_DIR, TRAINING_BLACK_CHARIOT_DIR, VALIDATION_BLACK_CHARIOT_DIR, split_size)
    split_data(BLACK_ELEPHANT_SOURCE_DIR, TRAINING_BLACK_ELEPHANT_DIR, VALIDATION_BLACK_ELEPHANT_DIR, split_size)
    split_data(BLACK_Knight_SOURCE_DIR, TRAINING_BLACK_Knight_DIR, VALIDATION_BLACK_Knight_DIR, split_size)
    split_data(BLACK_KING_SOURCE_DIR, TRAINING_BLACK_KING_DIR, VALIDATION_BLACK_KING_DIR, split_size)
    split_data(BLACK_PAWN_SOURCE_DIR, TRAINING_BLACK_PAWN_DIR, VALIDATION_BLACK_PAWN_DIR, split_size)
    split_data(RED_ADVISER_SOURCE_DIR, TRAINING_RED_ADVISER_DIR, VALIDATION_RED_ADVISER_DIR, split_size)
    split_data(RED_CANNON_SOURCE_DIR, TRAINING_RED_CANNON_DIR, VALIDATION_RED_CANNON_DIR, split_size)
    split_data(RED_CHARIOT_SOURCE_DIR, TRAINING_RED_CHARIOT_DIR, VALIDATION_RED_CHARIOT_DIR, split_size)
    split_data(RED_ELEPHANT_SOURCE_DIR, TRAINING_RED_ELEPHANT_DIR, VALIDATION_RED_ELEPHANT_DIR, split_size)
    split_data(RED_Knight_SOURCE_DIR, TRAINING_RED_Knight_DIR, VALIDATION_RED_Knight_DIR, split_size)
    split_data(RED_KING_SOURCE_DIR, TRAINING_RED_KING_DIR, VALIDATION_RED_KING_DIR, split_size)
    split_data(RED_PAWN_SOURCE_DIR, TRAINING_RED_PAWN_DIR, VALIDATION_RED_PAWN_DIR, split_size)

    # Your function should perform copies rather than moving images so original directories should contain unchanged images
    print(f"Original Black Adviser directory has {len(os.listdir(BLACK_ADVISER_SOURCE_DIR))} images\n")
    print(f"Original Black Cannon directory has {len(os.listdir(BLACK_CANNON_SOURCE_DIR))} images\n")
    print(f"Original Black Chariot directory has {len(os.listdir(BLACK_CHARIOT_SOURCE_DIR))} images\n")
    print(f"Original Black Elephant directory has {len(os.listdir(BLACK_ELEPHANT_SOURCE_DIR))} images\n")
    print(f"Original Black Knight directory has {len(os.listdir(BLACK_Knight_SOURCE_DIR))} images\n")
    print(f"Original Black King directory has {len(os.listdir(BLACK_KING_SOURCE_DIR))} images\n")
    print(f"Original Black Pawn directory has {len(os.listdir(BLACK_PAWN_SOURCE_DIR))} images\n")
    print(f"Original Red Adviser directory has {len(os.listdir(RED_ADVISER_SOURCE_DIR))} images\n")
    print(f"Original Red Cannon directory has {len(os.listdir(RED_CANNON_SOURCE_DIR))} images\n")
    print(f"Original Red Chariot directory has {len(os.listdir(RED_CHARIOT_SOURCE_DIR))} images\n")
    print(f"Original Red Elephant directory has {len(os.listdir(RED_ELEPHANT_SOURCE_DIR))} images\n")
    print(f"Original Red Knight directory has {len(os.listdir(RED_Knight_SOURCE_DIR))} images\n")
    print(f"Original Red King directory has {len(os.listdir(RED_KING_SOURCE_DIR))} images\n")
    print(f"Original Red Pawn directory has {len(os.listdir(RED_PAWN_SOURCE_DIR))} images\n")

    # generate_data()

    # Training and validation splits. Check that the number of images matches the expected output.
    print(f"There are {len(os.listdir(TRAINING_BLACK_ADVISER_DIR))} images of cats for training")
    print(f"There are {len(os.listdir(TRAINING_BLACK_CANNON_DIR))} images of dogs for training")
    print(f"There are {len(os.listdir(TRAINING_BLACK_CHARIOT_DIR))} images of cats for training")
    print(f"There are {len(os.listdir(TRAINING_BLACK_ELEPHANT_DIR))} images of dogs for training")
    print(f"There are {len(os.listdir(TRAINING_BLACK_Knight_DIR))} images of cats for training")
    print(f"There are {len(os.listdir(TRAINING_BLACK_KING_DIR))} images of dogs for training")
    print(f"There are {len(os.listdir(TRAINING_BLACK_PAWN_DIR))} images of cats for training")
    print(f"There are {len(os.listdir(TRAINING_RED_ADVISER_DIR))} images of dogs for training")
    print(f"There are {len(os.listdir(TRAINING_RED_CANNON_DIR))} images of cats for training")
    print(f"There are {len(os.listdir(TRAINING_RED_CHARIOT_DIR))} images of dogs for training")
    print(f"There are {len(os.listdir(TRAINING_RED_ELEPHANT_DIR))} images of cats for training")
    print(f"There are {len(os.listdir(TRAINING_RED_Knight_DIR))} images of dogs for training")
    print(f"There are {len(os.listdir(TRAINING_RED_KING_DIR))} images of cats for training")
    print(f"There are {len(os.listdir(TRAINING_RED_PAWN_DIR))} images of dogs for training")

    print(f"There are {len(os.listdir(VALIDATION_BLACK_ADVISER_DIR))} images of Black Adviser for validation")
    print(f"There are {len(os.listdir(VALIDATION_BLACK_CANNON_DIR))} images of Black Cannon for validation")
    print(f"There are {len(os.listdir(VALIDATION_BLACK_CHARIOT_DIR))} images of Black Chariot for validation")
    print(f"There are {len(os.listdir(VALIDATION_BLACK_ELEPHANT_DIR))} images of Black Elephant for validation")
    print(f"There are {len(os.listdir(VALIDATION_BLACK_Knight_DIR))} images of Black Knight for validation")
    print(f"There are {len(os.listdir(VALIDATION_BLACK_KING_DIR))} images of Black King for validation")
    print(f"There are {len(os.listdir(VALIDATION_BLACK_PAWN_DIR))} images of Black Pawn for validation")
    print(f"There are {len(os.listdir(VALIDATION_RED_ADVISER_DIR))} images of Red Adviser for validation")
    print(f"There are {len(os.listdir(VALIDATION_RED_CANNON_DIR))} images of Red Cannon for validation")
    print(f"There are {len(os.listdir(VALIDATION_RED_CHARIOT_DIR))} images of Red Chariot for validation")
    print(f"There are {len(os.listdir(VALIDATION_RED_ELEPHANT_DIR))} images of Red Elephant for validation")
    print(f"There are {len(os.listdir(VALIDATION_RED_Knight_DIR))} images of dogs Red Knight validation")
    print(f"There are {len(os.listdir(VALIDATION_RED_KING_DIR))} images of Red King for validation")
    print(f"There are {len(os.listdir(VALIDATION_RED_PAWN_DIR))} images of Red Pawn for validation")

    return TRAINING_DIR, VALIDATION_DIR


# def generate_data():
#     classes = os.listdir('.\\ChessChampImages')
#     count_image = 0
#     for class1 in classes:
#         images = os.listdir(os.path.join('.\\ChessChampImages', class1))
#         print("<image rotating process> <", class1, "> ======================================")
#         class_path = '.\\ChessChampImages360' + "\\" + class1
#         image_index = 0
#         for image in images:
#             img = Image.open(os.path.join(os.path.join('.\\ChessChampImages', class1), image))
#             for i in range(0, 360, 2):
#                 img_ro = img.rotate(i)
#                 image_index += 1
#                 each_image_path = class_path + "\\" + str(image_index) + "_" + class1 + ".jpg"
#                 # print(each_image_path)
#                 img_ro.save(each_image_path)
#                 count_image += 1
#         # print(str(count_image) + " image generated")
