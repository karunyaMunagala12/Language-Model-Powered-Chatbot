import json
import os

def parse_slide_content(file_path):
    slides = []
    current_slide = {}
    content = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Slide Number:'):
                if current_slide:
                    current_slide['content'] = content
                    slides.append(current_slide)
                
                current_slide = {'slideNumber': line.split(':')[1].strip()}
                content = []
            elif line.startswith('Title:'):
                current_slide['title'] = line.split('Title:')[1].strip()
            elif line:
                content.append(line)

        if current_slide:
            current_slide['content'] = content
            slides.append(current_slide)

    return slides

def process_lectures(root_dir):
    lectures = []
    for lecture_name in os.listdir(root_dir):
        lecture_dir = os.path.join(root_dir, lecture_name)
        if os.path.isdir(lecture_dir):
            for file_name in os.listdir(lecture_dir):
                if file_name.endswith('.txt'):
                    file_path = os.path.join(lecture_dir, file_name)
                    slides = parse_slide_content(file_path)
                    lectures.append({
                        "lectureName": lecture_name,
                        "slides": slides
                    })
    return lectures

root_dir = 'Lecture_Notes'
lectures = process_lectures(root_dir)
final_json = json.dumps({"Lecture_Notes": lectures}, indent=2)

# To save the JSON to a file
with open('Lecture_Notes.json', 'w') as json_file:
    json_file.write(final_json)

# print(final_json)
