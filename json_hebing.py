import json
import os


def merge_coco_jsons(input_dir, output_path):
    """
    合并指定文件夹下的多个COCO格式JSON文件，并保存到指定路径。

    参数：
    - input_dir: str, 包含多个JSON文件的文件夹路径
    - output_path: str, 合并后JSON文件的保存路径
    """
    # 获取文件夹下所有JSON文件
    json_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.json')]
    if not json_files:
        raise ValueError("指定文件夹中没有找到JSON文件！")

    # 初始化合并后的COCO字典
    merged_coco = {
        "info": {},
        "licenses": [],
        "categories": [],
        "images": [],
        "annotations": []
    }

    # 从第一个JSON文件读取info, licenses, categories
    with open(json_files[0], 'r', encoding='utf-8') as f:
        first_coco = json.load(f)
        merged_coco['info'] = first_coco.get('info', {})
        merged_coco['licenses'] = first_coco.get('licenses', [])
        merged_coco['categories'] = first_coco.get('categories', [])  # 假设标注种类一致

    # 初始化ID偏移量
    image_id_offset = 0
    annotation_id_offset = 0

    # 遍历每个JSON文件进行合并
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            coco = json.load(f)

        # 图像ID映射
        image_id_map = {}
        for image in coco['images']:
            old_id = image['id']
            new_id = old_id + image_id_offset
            image_id_map[old_id] = new_id
            image['id'] = new_id
            merged_coco['images'].append(image)

        # 标注ID映射
        for annotation in coco['annotations']:
            old_id = annotation['id']
            new_id = old_id + annotation_id_offset
            annotation['id'] = new_id
            # 更新image_id为新的映射值
            annotation['image_id'] = image_id_map[annotation['image_id']]
            merged_coco['annotations'].append(annotation)

        # 更新偏移量，确保下一轮ID不重复
        if coco['images']:
            image_id_offset = max(image_id_offset, max([img['id'] for img in coco['images']])) + 1
        if coco['annotations']:
            annotation_id_offset = max(annotation_id_offset, max([ann['id'] for ann in coco['annotations']])) + 1

    # 确保输出文件夹存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 保存合并后的JSON文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_coco, f, indent=4)
    print(f"合并完成，文件已保存至：{output_path}")


# 示例调用
if __name__ == "__main__":
    input_directory = r"C:\python work\ultralytics-yolo11-main-20250205\label\tests"  # 替换为你的JSON文件所在文件夹路径
    output_file = r"C:\python work\ultralytics-yolo11-main-20250205\label\test\merged.json"  # 替换为合并后文件的保存路径
    merge_coco_jsons(input_directory, output_file)