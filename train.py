import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

#يستخد لتحويل الكلمات الى صيغتها الاساسية في اللغة الانكليزية اي يعيد الكلمة الى جزرها
lemmatizer = WordNetLemmatizer()
#قراءة الملف الذي يحوي الاسئلة والاجوبة المحتملة
intents = json.loads(open('intents.json').read())

#تحوي الكلمات للاسئلة
words = []
#تحوي اسماء التاغات
classes = []
#تحوي اسماء التاغات والكلمات المفتاحية للاسئلة
documents = []
ignore_letters = ['?', '!',',','.']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        #تحلل النص الموجود في متغير "باترن" ولتحويله الى قائمة من الكلمات المفردة
        # تستخدم هذه القائمة في عمليات التحليل اللغوي للنص او البحث عن كلمات معينة
        word_list = nltk.word_tokenize(pattern)
        #print(word_list)
        words.extend(word_list)
        documents.append((word_list,intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

#تحفظ قائمة الكلمات في ملف باسمه ويتم فتح الملف في وضع الكتابة الثنائية باينري
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))
#تستخدم هذه القائمة لتخزين النتائج النهائية للتنبؤ بالفئة التي ينتمي إليها كل عنصر في البيانات
training = []
# تنشا قائمة تحوي عدد من الاصفار يساوي عدد الفئات المختلفة المجودة في البيانات
output_empty = [0] * len(classes)

for document in documents:
    #وتستخدم هذه القائمة لتخزين معلومات حول الكلمات التي توجد في كل عنصر
    #تدل على كلمات المفتاحية للسوال
    bag =[]
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    #للانتقال عبر كل كلمة في النص، وإضافة 1 إلى قائمة bag إذا كانت الكلمة موجودة في النص، وإلا يتم إضافة 0.
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    #ستخدم هذه القائمة لتخزين النتائج النهائية لكل عنصر في البيانات. يتم تعيين القيمة 1 في الموضع المناسب في output_row إذا كان العنصر ينتمي إلى الفئة المحددة، وإلا يتم تعيين القيمة 0.
    #تتعامل مع التاغ
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])
#ستخدم لتبديل عناصر قائمة التدريب بشكل عشوائي هذا يساعد في تجنب الانحياز في التدريب وضمان تنوع البيانات المستخدمة في التدريب
random.shuffle(training)

training = np.array(training,dtype=object)

#اول عنصر بالترينينغ يدل على الكلمات المفتاحية للسوال وتاني عنصر يدل على التاغ
train_x = list(training[:, 0])
train_y = list(training[:, 1])

# انشاء نموذج باستخدام الشبكة العصبية التسلسلية
model = Sequential()

model.add(Dense(128, input_shape=(len(train_x[0]),),activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(learning_rate=0.01,momentum=0.9,nesterov=True)


model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbotmodel.h5', hist)

print('Done')