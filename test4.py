import re, os
# path
PATH = os.path.dirname(os.path.abspath(__file__))
inputFolders = os.path.join(PATH, 'inputFolders')
outputAudio = os.path.join(PATH,'outputAudio')

os.makedirs(inputFolders, exist_ok=True)
os.makedirs(outputAudio, exist_ok=True)


# def remove_non_alphabetic_chars(string):
#     return re.sub(r'[^a-zA-Z0-9ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂẾưăạảấầẩẫậắằẳẵặẹẻẽềềểếỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹý\s\W|_!?\"\',.]+', '', string)
# with open('inputFolders\Chuong 103.txt', 'r', encoding='utf-8') as f:
#     string = f.read()
# result = remove_non_alphabetic_chars(string)
# print(result)

# string  = "Kêu xong tên, giọng Lăng Vô Cấu đột.... nhiên nghẹn              lại một chút, ánh mắt của hắn khóa chặt trên danh sách một chớp mắt, sau đó mới âm điệu quái dị tiếp tục kêu... ['. . .', '. .', '————','———','——', '-']:"

def formatText(text='', is_number = False):
    # remove any special character
    text = re.sub(r"[^\w~`!@$%^&*()<>?/\\\":'\s,.-;\[\{\}\]<>|+_\n]-"," ",text, flags=re.M)
    # remove number in [] like [1], [2],...
    text = re.sub(r"\[\d+\]", " ", text, flags=re.M)
    # replace any break line
    text = re.sub(r'\n+', '. ', text, flags=re.M).strip()
    # remove duplicate special character
    text = re.sub(r'[^\w\s][^\w\s]+', '. ', text, flags=re.M)
    # remove number
    if is_number:
        text = re.sub(r'\d+', '. ', text, flags=re.M)
    # replace chuong like chuong1: abc to chuong 1. abc
    result = re.search(r'^Chương\b.\d+:*', text,flags=re.I)
    if result:
        text = text.replace(result.group(0), result.group(0) + '. ')
    return ' '.join(text.split())

chapter_name =  'Chuong 103 hay gì đó txt'
chapter_title = ' '.join(chapter_name.split('.')[0:-1]) if len(chapter_name.split('.')) > 1 else chapter_name.split('.')[-1]

print(chapter_title)