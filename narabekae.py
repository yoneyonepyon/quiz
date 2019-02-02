import csv
import datetime
import os
import random
import sys
import tkinter
import tkinter.filedialog



#文字列をランダムに並べ替えた文字列を返す関数
def anagram(str):
    #受け取った文字列を１文字ずつのリストにする
    str = list(str)
    
    #文字のリストをシャッフル
    random.shuffle(str)
    
    #リストから文字列に戻して返す
    return "".join(str)


print('問題ファイルを読み込んでください...')

# 問題ファイルを指定
root  = tkinter.Tk()
root.withdraw()
fname = tkinter.filedialog.askopenfilename(filetypes=[('data files','*.csv')],initialdir=os.getcwd())

#問題ファイルをリストに格納する
#quizzes[行][0=問題文 1=正解]
with open(fname, 'r', encoding="utf-8") as f:
    quizzes = [row for row in csv.reader(f)]
    
    
#問題をランダムに並べ替える
random.shuffle(quizzes)

#誤答リストを準備
wrong_answer = []
print('\n読み込み完了しました\n')
print(str(len(quizzes)) + '問出題します')



#順番に出題する
count = 1
for quiz in quizzes:
    
#問題文を表示
    print('終了したいときは終了と入力してください')
    print('-' * 100)
    print('第{0}問：{1}'.format(count, quiz[0]))
    print('-' * 100)

#正解のアナグラムを表示
    print(anagram(quiz[1]))
    print('-' * 100)

#回答を入力して正解と比較
    answer = input()
    if answer == '終了':
        
        #中断した問題を無視してリザルトを出すため
        count -= 1 
        break;
    elif answer == quiz[1]:
        print('\n正解\n')
        count += 1
    else:
        print('\n不正解\n')
        print('正解は「{0}」です\n'.format(quiz[1]))
        
        # 誤答リストに追加
        wrong_answer.append(quiz)
        
        count += 1


# 1問目で終了するとリザルトは無意味なので出さずに終了する
if count == 0:
    sys.exit(0)

# 正解率を計算
rate = 1 - len(wrong_answer) / count

# リザルト
print('お疲れ様でした' + str(count) + '問中' + str(count-len(wrong_answer)) + '問正解しました')
print('正解率は' + str(int((rate*100))) + '%です。')
    
# 誤答リストを出力
if rate != 1:
    now = datetime.datetime.now()
    output_file_name = 'wa_{0:%Y}_{0:%m%d}_{0:%H}-{0:%M}-{0:%S}.csv'.format(now)

    with open(output_file_name, 'w', encoding="utf-8") as f:
       writer = csv.writer(f, lineterminator='\n')
       writer.writerows(wrong_answer)
       print('間違えた問題を「{0}」に出力したので復習してください。'.format(output_file_name))

