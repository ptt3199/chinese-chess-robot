import os
from PIL import Image
import g_params

number_angle = 360
IMAGE_SHOW = False
angle_step = 3


def clear(data_gen_path):
    one_level = os.listdir(data_gen_path)
    for two_level in one_level:
        temp_path = os.path.join(data_gen_path, two_level)
        temp_files = os.listdir(temp_path)
        print(two_level, " removed")
        for file in temp_files:
            os.remove(os.path.join(temp_path, file))


def generate_data(pre_generate, final_path):
    classes = os.listdir(pre_generate)
    count_image = 0
    for class1 in classes:
        images = os.listdir(os.path.join(pre_generate, class1))
        print("<image rotating process> <", class1, "> ======================================")
        # current_image_num = chess_map[each_group]
        # current_rotate_angle = 360.0 / current_image_num
        # current_rotate_angle = 360
        # current_rotate_number = current_rotate_angle * (number_angle / 360.0)
        # current_rotate_number = 360
        class_path = final_path + "\\" + class1
        image_index = 0
        for image in images:
            img = Image.open(os.path.join(os.path.join(pre_generate, class1), image))
            # start_angle = count_image * current_rotate_angle
            # start_angle = 0
            for i in range(0, 360, angle_step):
                # img_ro = img.rotate(start_angle + i * each_rotate_angle)
                img_ro = img.rotate(i)
                image_index += 1
                each_image_path = class_path + "\\" + str(image_index) + "_" + class1 + ".jpg"
                print(each_image_path)
                img_ro.save(each_image_path)
                count_image += 1
    print(str(count_image) + " image generated")


def main():
    pre_generate_path = g_params.pre_generate_path
    final_path = g_params.train_image_path
    clear(final_path)
    generate_data(pre_generate_path, final_path)


if __name__ == '__main__':
    main()
