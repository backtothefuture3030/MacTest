from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os, random, time, threading, winsound, copy, pickle
from datetime import datetime

# 리소스파일 경로를 상대경로로 지정하기위한 함수
# 스크립트 파일의 현재 위치를 기준으로 경로를 지정할 수 있음
def relpath(dir, cwd=None):
    if cwd is None:
        cwd = os.path.realpath(os.getcwd())
    dir = os.path.realpath(dir)
    cpfx = os.path.commonprefix([dir, cwd]).split(os.sep)
    if cpfx[-1] == '':
        del cpfx[-1]
    dirpaths = dir.split(os.sep)
    cwdpaths = cwd.split(os.sep)
    return os.sep.join(['..'] * (len(cwdpaths) - len(cpfx))
                + dirpaths[len(cpfx):])

# 카드 번호를 인수로 주면 해당되는 카드 이미지 파일의 상대경로 및 파일명을 반환
def image_path(number_of_card):
    path='resource\\'
    path=path+str(number_of_card)
    path=path+'.gif'
    return path

# 카드 덱 보여주기
# 카드 나열과 셔플링 사운드 출력을 동시에 실행하기 위해 두 개의 thread를 사용함
def show_deck():
    threads = []
    threads.append(threading.Thread(target=show_deck_image))
    threads.append(threading.Thread(target=play_deck_sound))
    threads[0].start()
    threads[1].start()
    for th in threads:
        th.join()

def show_deck_image():
    for x in range(0,len(deck)):
        deck_image.append(canvas.create_image(25+x*2.5,190, \
                                             anchor=NW, image=b1fv_image))
        deck_place.append(25+x*2.5)
        root.after(5,root.update())

def play_deck_sound():
    winsound.PlaySound(relpath('resource\\shuffling2.wav'), winsound.SND_ALIAS)

# Rank 계산 함수
def get_rank(cards_list):
    # =================== rank 순서 ===================
    # 기본적으로 한 족보당 20의 간격
    #  rank                  rank_name
    #---------  ---------------------------------------
    # 1~4     : 로얄스트레이트 플러시(10, J, Q, K, A)
    # 5~8     : 백스트레이트 플러시(A, 2, 3, 4, 5)
    # 9~20    : 스트레이트 플러시
    # 21~40   : 포카드
    # 41~60   : 풀하우스
    # 61~80   : 플러시
    # 81~100  : 스트레이트
    # 101~120 : 트리플
    # 121~140 : 투페어
    # 141~160 : 원페어
    # 180~200 : 노카드
    # =================================================


    # 가진 카드를 덱번호대로 정렬
    hand=copy.deepcopy(sorted(cards_list))

    # 카드 번호의 리스트를 만듬
    num = []
    for x in hand:
        if divmod(x, 13)[1] == 0:
            num.append(13)
        else:
            num.append(divmod(x, 13)[1])
    num.sort()

    # 노카드로 가정한 경우의 rank 먼저 기록
    rank = 200
    rank_name = "노카드"
    if min(num) == 1:
        rank = 180
    else:
        rank = 200 - max(num)

    # 1단계: 숫자 중복 족보 체크
    # 원페어(12th), 투페어(11th), 트리플(10th), 풀하우스(5th), 포카드(4th)
    # A~K까지 숫자별로 같은 숫자 카드가 총 몇개씩인지를 알려주는 리스트 생성
    k = []
    '''각 족보의 해당여부를 알려주는 BOOL변수 생성(중복해당가능)'''
    four_card = False
    full_house = False
    triple = False
    two_pair = False
    one_pair = False

    '''각 족보에 해당시 동순위의 승부를 가르기 위해 가장 높은 카드 숫자를 기록하는 변수 생성'''
    four_card_number = 0 # 포카드는 7장의 카드에서 1개까지만 가능하므로 int변수 사용
    triple_number = []   # 트리플은 7장의 카드에서 2개까지 가능하므로 리스트를 사용
    pair_number = []     # 페어는 7장의 카드에서 3개까지 가능하므로 리스트를 사용

    for x in range(1,14):
        k.append(num.count(x))
        '''만약 같은 숫자가 4개 있는 경우(포카드), 무슨 숫자의 포카드인지를 기록'''
        if num.count(x) == 4:
            four_card_number = x
        '''만약 같은 숫자가 3개 있는 경우(트리플), 무슨 숫자의 트리플인지를 기록'''
        if num.count(x) == 3:
            triple_number.append(x)
        '''만약 같은 숫자가 2개 있는 경우(페어), 무슨 숫자의 페어인지를 기록'''
        if num.count(x) == 2:
            pair_number.append(x)

    '''트리플과 페어 넘버의 경우 가장 큰 숫자가 맨 앞으로 가게 역순정렬함'''
    triple_number.reverse()
    pair_number.reverse()

    if four_card_number > 0:
        # 포카드(rank: 21 ~ 40)
        four_card = True
        if four_card_number == 1:
            if rank > 21:
                rank = 21
                rank_name = "포카드"
        else:
            if rank > 38:
                rank = 40 - four_card_number
                rank_name = "포카드"
    elif triple_number != []:
        if pair_number != []:
            # 풀하우스(rank: 41 ~ 60)
            if triple_number.count(1) == 1:
                if rank > 41:
                    rank = 41
                    rank_name = "풀하우스"
            else:
                if rank > 58:
                    rank = 60 - triple_number[0]
                    rank_name = "풀하우스"
        else:
            # 트리플(rank: 101 ~ 120)
            triple = True
            if triple_number.count(1) == 1:
                if rank > 101:
                    rank = 101
                    rank_name = "트리플"
            else:
                if rank > 118:
                    rank = 120 - triple_number[0]
                    rank_name = "트리플"
    elif pair_number != []:
        if k.count(2) > 1:
            # 투페어(rank: 121 ~ 140)
            two_pair = True
            if pair_number.count(1) >= 1:
                if rank > 121:
                    rank = 121
                    rank_name = "투페어"
            else:
                if rank > 138:
                    rank = 140 - pair_number[0]
                    rank_name = "투페어"
        else:
            # 원페어(rank: 141 ~ 160)
            one_pair = True
            if pair_number.count(1) == 1:
                if rank > 141:
                    rank = 141
                    rank_name = "원페어"
            else:
                if rank > 158:
                    rank = 160 - pair_number[0]
                    rank_name = "원페어"

    # 카드 무늬의 리스트를 만듬
    pattern=[]
    for x in hand:
        pattern.append(divmod(x-1, 13)[0])

    if four_card == True or full_house == True or len(hand) < 5:
        pass
        # 포카드이거나, 풀하우스이거나, 카드장수가 5장 미만이면
        # 스트레이트나 플러시가 될 가능성이 없음
    else:
        # 2단계: 무늬 중복 족보 체크: 플러시(rank: 61~80)
        flush = False
        if pattern.count(0) >= 5:
            rank=61
            rank_name = "스페이드 플러시"
            flush = True
        elif pattern.count(1) >= 5:
            rank=62
            rank_name = "다이아몬드 플러시"
            flush = True
        elif pattern.count(2) >= 5:
            rank=63
            rank_name = "하트 플러시"
            flush = True
        elif pattern.count(3) >= 5:
            rank=64
            rank_name = "클로버 플러시"
            flush = True

        # 이미 플러시인 경우 스트레이트만으로는 어차피 플러시보다 아래이므로
        # 스트레이트 검사는 스티플 이상인 경우에만 의미가 있음
        # 따라서 플러시를 이룬 다섯장만 남기고 나머지는 삭제한 뒤 스트레이트 검사를 해야 함
        delnum = 0 # 삭제한 카드의 장수를 기록해놓는 변수
        if flush:
            if rank_name == "스페이드 플러시":
                pattern_num = 0
                for x in range(0,len(hand)):
                    if pattern[len(hand)-1-x] != pattern_num:
                        del hand[len(hand)-1-x]
                        delnum+=1
            elif rank_name == "다이아몬드 플러시":
                pattern_num = 1
                for x in range(0,len(hand)):
                    if pattern[len(hand)-1-x] != pattern_num:
                        del hand[len(hand)-1-x]
                        delnum+=1
            elif rank_name == "하트 플러시":
                pattern_num = 2
                for x in range(0,len(hand)):
                    if pattern[len(hand)-1-x] != pattern_num:
                        del hand[len(hand)-1-x]
                        delnum+=1
            elif rank_name == "클로버 플러시":
                pattern_num = 3
                for x in range(0,len(hand)):
                    if pattern[len(hand)-1-x] != pattern_num:
                        del hand[len(hand)-1-x]
                        delnum+=1
            num=[]
            for x in hand:
                if divmod(x, 13)[1] == 0:
                    num.append(13)
                else:
                    num.append(divmod(x, 13)[1])
            num.sort()

        # 3단계: 숫자 연속 족보 체크
        # 스트레이트, 백스트레이트, 마운틴(rank: 81~100)
        straight_top_number = 0
        straight = False
        backstraight = False
        mountain = False

        num_no_repeat = num # 중복숫자를 제거한 숫자 리스트 생성
        num_ace_to_fourteen =[] # A를 14로 바꾼 숫자 리스트 생성

        # 플러시인 경우에는 무늬가 같은 다섯장의 카드만 남고 삭제되므로
        # 같은 번호가 있을 수 없음. 따라서 아래의 중복제거는 delnum이 항상 0인 상태로
        # 시작됨
        i=0
        for x in range(0,len(hand)-delnum-1):
            if num_no_repeat[len(hand)-1-delnum-x] == num_no_repeat[len(hand)-2-delnum-x]:
                del num_no_repeat[len(hand)-1-delnum-x]
                i+=1
        delnum+=i

        num_ace_to_fourteen = copy.deepcopy(num_no_repeat)
        if num_ace_to_fourteen[0] == 1:
            num_ace_to_fourteen[0] = 14
        num_ace_to_fourteen.sort()
        for x in range(0,len(hand)-4-delnum):
            if (num_no_repeat[x+1] - num_no_repeat[x] == 1) and \
               (num_no_repeat[x+2] - num_no_repeat[x+1] == 1) and\
               (num_no_repeat[x+3] - num_no_repeat[x+2] == 1) and\
               (num_no_repeat[x+4] - num_no_repeat[x+3] == 1):
                straight = True
                straight_top_number = num_no_repeat[x+4]
                if rank > 100:
                    rank = 100 - straight_top_number
                    rank_name = "스트레이트"
                if num_no_repeat[x] == 1:
                    backstraight = True
                    if rank > 82:
                        rank = 82
                        rank_name = "백스트레이트"

        for x in range(0,len(hand)-4-delnum):
            if (num_ace_to_fourteen[x+1] - num_ace_to_fourteen[x] == 1) and \
               (num_ace_to_fourteen[x+2] - num_ace_to_fourteen[x+1] == 1) and\
               (num_ace_to_fourteen[x+3] - num_ace_to_fourteen[x+2] == 1) and\
               (num_ace_to_fourteen[x+4] - num_ace_to_fourteen[x+3] == 1):
                straight = True
                straight_top_number = num_ace_to_fourteen[x+4]
                if rank > 100:
                    rank = 100 - straight_top_number
                    rank_name = "스트레이트"
                if num_ace_to_fourteen[x] == 10:
                    mountain = True
                    if rank >81:
                        rank = 81
                        rank_name = "마운틴"

        # 4단계: 스트레이트와 플러시의 복합 족보 체크
        # 스트레이트 플러시(rank: 9~20)
        # 백스트레이트 플러시(rank: 5~8)
        # 로얄스트레이트 플러시(rank: 1~4)
        if backstraight and flush:
            rank = 5 + pattern_num
            rank_name = "백스트레이트 플러시"
        elif mountain and flush:
            rank = pattern_num + 1
            rank_name = "로얄스트레이트 플러시"
        elif straight and flush:
            rank = 20 - max(num_no_repeat)
            rank_name = "스트레이트 플러시"

    # 최종 rank와 rank_name을 튜플에 담아 리턴함
    return (rank, rank_name)

# Player1(사용자)이 받은 카드의 이미지를 버튼으로 만들어 보여주기
''' renew가 True로 지정된 경우에는 기존의 버튼을 제거하고 처음부터 다시 생성 '''
''' card_images 리스트를 호출할 때 카드의 숫자에서 1을 뺀 값을 넣는 것에 주의 '''
def show_cards_p1(renew=False,clicked=0):
    if clicked == 3: # 세번째장을 클릭한 경우: 이동 불필요
            pass
    else:
        if renew:
            if clicked == 1: # moving between 1st and 3rd card
                start_x = float(p1_slot[0].place_info()['relx'])*table_width
                end_x = float(p1_slot[2].place_info()['relx'])*table_width
                delta_x = (end_x - start_x)/10
                y = float(p1_slot[0].place_info()['rely'])*table_height
                for i in range(0,10):
                    p1_slot[0].place(relx = (start_x + delta_x*i)/table_width, \
                                      rely = y/table_height)
                    p1_slot[2].place(relx = (end_x - delta_x*i)/table_width, \
                                      rely = y/table_height)
                    root.after(10, root.update())
            elif clicked == 2: # moving between 2nd and 3rd card
                start_x = float(p1_slot[1].place_info()['relx'])*table_width
                end_x = float(p1_slot[2].place_info()['relx'])*table_width
                delta_x = (end_x - start_x)/10
                y = float(p1_slot[1].place_info()['rely'])*table_height
                for i in range(0,11):
                    p1_slot[1].place(relx = (start_x + delta_x*i)/table_width, \
                                      rely = y/table_height)
                    p1_slot[2].place(relx = (end_x - delta_x*i)/table_width, \
                                      rely = y/table_height)
                    root.after(10, root.update())
            if clicked <= 2: # show 1st and 2nd hidden cards
                for x in range(0,3):
                    p1_slot[x].destroy()
                del p1_slot[0:3]

                for x in range(0,3):
                    p1_slot.append(Button(root,image=card_images[p1_cards[x]-1], \
                    anchor='nw', borderwidth=0, highlightthickness=0))
                    p1_slot[x].pack()
                    p1_slot[x].place(relx = (card_start_width_p1 + between_cards*x)/table_width, \
                                         rely = card_start_height_p1/table_height)
                    root.update()
            if clicked == 7: # flip of 7th cards
                show_flip(1, p1_slot, p1_cards, 6)
        else:
            temp2=len(p1_slot)
            for x in range(temp2,len(p1_cards)):
                canvas.delete(deck_image[-1])
                del deck_image[-1]
                start_x = deck_place[-1]
                del deck_place[-1]
                if temp2 == 6: # last card(hidden)
                    p1_slot.append(Button(root,image=b1fv_image, anchor='nw', \
                    borderwidth=0, highlightthickness=0))
                    p1_slot[6].config(command = f7)
                else:
                    p1_slot.append(Button(root,image=card_images[p1_cards[x]-1], \
                    anchor='nw', borderwidth=0, highlightthickness=0))
                p1_slot[x].pack()

                # card distribution animation(from deck to slot)
                p1_slot[x].place(relx = start_x/table_width, \
                                 rely = 190/table_height)
                delta_x = ((card_start_width_p1 + between_cards*x) - start_x)/10
                delta_y = (card_start_height_p1 - 190)/10
                for i in range(0,11):
                    p1_slot[-1].place(relx = (start_x + delta_x*i)/table_width, \
                                      rely = (190 + delta_y*i)/table_height)
                    root.after(10, root.update())
                winsound.PlaySound(relpath('resource\\whoo2.wav'), winsound.SND_ALIAS)

#Player2(컴퓨터)가 받은 카드 이미지 보여주기
def show_cards_p2(renew = False):
    if renew:
        for x in [0,1,6]: # 히든카드(3장) 뒤집기
            if x == 0:
                time.sleep(0.5)
            canvas.itemconfig(p2_slot[x], image=card_images[p2_cards[x]-1])
            winsound.PlaySound(relpath('resource\\whoo2.wav'), winsound.SND_ALIAS)
            root.update()
    else:
        temp2=len(p2_slot)
        if temp2 != 0:
            time.sleep(0.3)
        for x in range(temp2,len(p2_cards)):
            if x < 2 or x == 6:
                canvas.delete(deck_image[-1])
                del deck_image[-1]
                start_x = deck_place[-1]
                del deck_place[-1]
                p2_slot.append(canvas.create_image(\
                    start_x, 190, image=b1fv_image, anchor='nw'))
                delta_x = ((card_start_width_p2 - between_cards*x) - start_x)/10
                delta_y = (card_start_height_p2 - 190)/10
                for i in range(0,10):
                    canvas.move(p2_slot[-1], delta_x, delta_y)
                    root.after(10, root.update())
                winsound.PlaySound(relpath('resource\\whoo2.wav'), \
                winsound.SND_ALIAS)
            else:
                canvas.delete(deck_image[-1])
                del deck_image[-1]
                start_x = deck_place[-1]
                del deck_place[-1]
                p2_slot.append(canvas.create_image(\
                    start_x, 190, image=card_images[p2_cards[x]-1], anchor='nw'))
                delta_x = ((card_start_width_p2 - between_cards*x) - start_x)/10
                delta_y = (card_start_height_p2 - 190)/10
                for i in range(0,10):
                    canvas.move(p2_slot[-1], delta_x, delta_y)
                    root.after(10, root.update())
                winsound.PlaySound(relpath('resource\\whoo2.wav'), \
                winsound.SND_ALIAS)

# show halo image
def show_halo():
    while len(p1_cards) < 4:
        halo = canvas.create_image(card_start_width_p1 - 5, \
          card_start_height_p1 - 6, image = halo_1_im, anchor = 'nw')
        root.update()
        root.after(200, canvas.delete(halo))
        root.update()
        root.after(200,)

# 카드(이미지 또는 버튼) 뒤집기 함수
# num은 해당 카드 첫 장 부터 0, 1, 2...순으로 세었을 때의 번호
def show_flip(player_num = 1, slot_name = None, cards_list_name = None, num = 0):
    if player_num == 1:
        x = card_start_width_p1 + between_cards*num
        y = card_start_height_p1
    else:
        x = card_start_width_p2 - between_cards*num
        y = card_start_height_p2

    back_file = Image.open(relpath('resource\\b1fv.gif'))
    front_file = Image.open(image_path(cards_list_name[num]))
    width, height = back_file.size
    size = []
    size.append(width)
    size.append(height)

    # 위젯 사이즈를 저장한 뒤 원래 위젯은 화면에서 지움
    if player_num == 1:
        slot_name[num].destroy()
        del slot_name[num]
    else:
        canvas.delete(slot_name[num])

    # step1. 뒷장 보여주기
    for i in range(0,width//5):
        size[0] = width - i*5
        im = ImageTk.PhotoImage(back_file.resize(size))
        bt_flip = Button(root, image=im, anchor=NW, borderwidth=0, \
        highlightthickness=0)
        bt_flip.pack()
        bt_flip.place(relx=(x+width/2-size[0]/2)/table_width, rely=y/table_height)
        root.update()
        root.after(10, bt_flip.destroy())

    # step2. 앞장 보여주기
    for i in range(0,width//5):
        size[0] = i*5
        im = ImageTk.PhotoImage(front_file.resize(size))
        slot_name.insert(num, Button(root, image=im, anchor=NW, borderwidth=0, \
        highlightthickness=0))
        slot_name[num].pack()
        slot_name[num].place(relx=(x+width/2-size[0]/2)/table_width, rely=y/table_height)
        root.update()
        if i != range(0,width//5)[-1]:
            root.after(10, )
            slot_name[num].destroy()
            del slot_name[num]
        else:
            slot_name[num].destroy()
            del slot_name[num]
            size[0] = width
            global flipped_image
            flipped_image = PhotoImage(file = relpath(image_path(cards_list_name[num])))
            slot_name.insert(num, Button(root, image = flipped_image, anchor=NW,\
             borderwidth=0, highlightthickness=0))
            slot_name[num].pack()
            slot_name[num].place(relx=x/table_width, rely=y/table_height)
            root.update()

# Player2가 어떤 카드를 오픈할 지 결정하는 함수
''' 일단은 랜덤하게 오픈하는 것으로 함 - 추후 인공지능 반영 요망 '''
def open_which_card():
    return random.randint(0,2)

# 버튼을 누르는 경우 실행되는 함수
def f1():
    p1_cards[0], p1_cards[2] = p1_cards[2], p1_cards[0]
    show_cards_p1(renew = True, clicked = 1)
    for x in range(0,2):
        p1_slot[x].config(state='disabled')
    root.after(1000, get_more_card())

def f2():
    p1_cards[1], p1_cards[2] = p1_cards[2], p1_cards[1]
    show_cards_p1(renew = True, clicked = 2)
    for x in range(0,2):
        p1_slot[x].config(state='disabled')
    root.after(1000, get_more_card())

def f3():
    if p1_slot[0]['state'] != 'disabled':
        show_cards_p1(renew = True, clicked = 3)
        for x in range(0,2):
            p1_slot[x].config(state='disabled')
        root.after(1000, get_more_card())

def f7():
    show_cards_p1(renew = True, clicked = 7)
    p1_slot[6].config(state='disabled')

def who_is_master():
    global who_wins
    rank1 = get_rank(p1_cards[2:len(p1_cards)])[0]
    rank2 = get_rank(p2_cards[2:len(p2_cards)])[0]
    if rank1 < rank2:
        who_wins[1].append(1)
    elif rank1 > rank2:
        who_wins[1].append(2)
    elif rank1 > 120 and rank1 < 140: # 같은 숫자 투페어일 때
        pass # 미완성
    elif rank1 > 140 and rank1 < 160: # 같은 숫자 원페어일 때
        pass # 미완성
    elif rank1 > 180 and rank1 < 200: # 같은 top숫자 노카드일 때
        num1 = []
        num2 = []
        for x in p1_cards:
            if divmod(x, 13)[1] == 0:
                num1.append(13)
            else:
                num1.append(divmod(x, 13)[1])
        for x in p2_cards:
            if divmod(x, 13)[1] == 0:
                num2.append(13)
            else:
                num2.append(divmod(x, 13)[1])
        num1.sort()
        num2.sort()
        for x in range(0,len(p1_cards)):
            if num1[x] > num2[x]:
                who_wins[1].append(1)
                break
        else:
            who_wins[1].append(1) # 모든 숫자까지도 같은 경우

# 추가 카드를 나눠주고 각 단계별 베팅 프로세스를 출발시키는 함수
def get_more_card():
    # 카드를 먼저받을 선 정하기
    global who_wins
    if len(p1_cards) == 0: # 새 게임이 시작되면 이전 판의 승자가 일단 선이 됨
        if who_wins[0][-1] != 0:
            who_wins[1].append(who_wins[0][-1])
    if len(p1_cards) == 3:
        who_is_master()

    # 이미 모든 카드를 받은 경우
    if len(p1_cards) == 7:
        show_cards_p2(renew = True)
        show_win_or_lose()

    # 카드 나눠주기
    if len(p1_cards) < 7:
        if who_wins[1][-1] == 1:
            p1_cards.append(deck[0])
            del deck[0]
            p2_cards.append(deck[0])
            del deck[0]
            show_cards_p1()
            show_cards_p2()
        elif who_wins[1][-1] == 2:
            p2_cards.append(deck[0])
            del deck[0]
            p1_cards.append(deck[0])
            del deck[0]
            show_cards_p2()
            show_cards_p1()
        if len(p1_cards) < 7: # 마지막 카드까지 받았으면 master를 업데이트할 필요 없음
            who_is_master()   # 그 외에는 카드를 새로 받았으니 master도 업데이트해야함
        # 베팅프로세스 촉발하기(매 stage 마다 한 번씩만 실행)
        bet.bet_process(who_wins[1][-1], len(p1_cards))

# 승패 표시 함수
def show_win_or_lose():
    global who_wins
    time.sleep(0.5)
    p1_rank, p1_rank_name = get_rank(p1_cards)
    p2_rank, p2_rank_name = get_rank(p2_cards)
    canvas.create_text(500, 200, anchor='w', fill='yellow', \
                       font=("Times", 15, 'bold'), text='Com    :')
    canvas.create_text(600, 200, anchor='w', fill='yellow', \
                       font=("Times", 15, 'bold'), text=p2_rank_name)
    canvas.create_text(500, 230, anchor='w', fill='yellow', \
                       font=("Times", 15, 'bold'), text='Player :')
    canvas.create_text(600, 230, anchor='w', fill='yellow', \
                       font=("Times", 15, 'bold'), text=p1_rank_name)
    root.update()
    time.sleep(1)
    if p1_rank < p2_rank:
        who_wins[0].append(1)
        text = canvas.create_text(500, 270, anchor='w', fill='yellow',\
                                  font=("Times",20, 'bold'), text='Player wins')
    elif p1_rank > p2_rank:
        who_wins[0].append(2)
        text = canvas.create_text(500, 270, anchor='w', fill='yellow', \
                                  font=("Times",20, 'bold'), text='Com wins')
    else: # 같은 rank인 경우
        who_wins[0].append(0)
        text = canvas.create_text(500, 270, anchor='w', fill='yellow', \
                                  font=("Times",20, 'bold'), text='Draw')
    for x in range(90):
        canvas.move(text, 1, 0)
        root.after(10,root.update())
    bet.close_money()

class Bet():
    def __init__(self):
        # 게임칩 관련 변수 생성
        self.chips = []
        self.chips.append([0,0,0,0,0])  # betting chips
        self.chips.append([0,0,0,0,0]) # player's chips
        self.chips.append([0,0,0,0,0]) # com's chips

        # 게임머니 관련 변수 생성
        self.money = [0,5000,5000]
        self.money_betted = [0,0,0]
        self.base_bet = 2

        self.chip_image = []
        self.chip_image.append(PhotoImage(file=relpath('resource\\chip_gold_30.gif')))
        self.chip_image.append(PhotoImage(file=relpath('resource\\chip_black_30.gif')))
        self.chip_image.append(PhotoImage(file=relpath('resource\\chip_red_30.gif')))
        self.chip_image.append(PhotoImage(file=relpath('resource\\chip_blue_30.gif')))
        self.chip_image.append(PhotoImage(file=relpath('resource\\chip_green_30.gif')))

        self.chips_im = []
        self.chips_txt = []
        self.show_bet_button()

        # 각 stage별로 몇번째 레이즈인지를 기록하는 변수 생성(0~4)
        self.betnum = 0

        # game level variable which decides maximum manual betting limit
        self.level = 1

    def getBetlimit(self):
        self.level = self.money[1]//100000 + 1
        self.level = min(5, self.level)      # maximum level is 5
        return (self.money[1]//5)*self.level # at level 5, player can do all-in

    def show_message(self, side = 0, message = None):
        if side == 0:
            text = canvas.create_text(300, 200, anchor='w', fill='yellow', \
                                      font=("Times",18, 'bold'), text = message)
            for x in range(30):
                canvas.move(text, 1, 0)
                root.after(10,root.update())
            root.after(1000,canvas.delete(text))
            root.update()
        elif side == 1: # player
            self.bettxt_p1 = canvas.create_text(650, 350, anchor='w', fill='yellow', \
                                      font=("Times",18, 'bold'), text = message)
            root.update()
            root.after(1000,)
            root.update()
        elif side == 2: # computer
            self.bettxt_p2 = canvas.create_text(650, 70, anchor='w', fill='yellow', \
                                      font=("Times",18, 'bold'), text = message)
            root.update()
            root.after(1000,)
            root.update()

    def show_bet_button(self):
        # 베팅버튼 공통좌표
        bet_b_x = 200
        bet_b_y = 435
        btw_bet_b = 50
        btcolor1 = 'Dim Gray'
        btcolor2 = 'orange'

        # fold button
        self.bt_die = Button(root, text="Fold", state = 'disabled', \
          command = lambda: self.die(1), width = 5, height = 3, bd = 3, \
          bg = btcolor1, activebackground = btcolor2)
        self.bt_die.pack()
        self.bt_die.place(relx=(bet_b_x + btw_bet_b*0)/table_width, \
          rely=bet_b_y/table_height)

        # call button
        self.bt_call = Button(root, text = "Call", state = 'disabled', \
          command = lambda: self.call(1), width = 5, height = 3, bd = 3, \
          bg = btcolor1, activebackground = 'green')
        self.bt_call.pack()
        self.bt_call.place(relx=(bet_b_x + btw_bet_b*1)/table_width, \
          rely=bet_b_y/table_height)

        # check button
        self.bt_check = Button(root, text="Check", state = 'disabled', \
          command = lambda: self.check(1), width = 5, height = 3, bd = 3, \
          bg = btcolor1, activebackground = btcolor2)
        self.bt_check.pack()
        self.bt_check.place(relx=(bet_b_x + btw_bet_b*2)/table_width, \
                            rely=bet_b_y/table_height)

        # quarter button
        self.bt_quarter = Button(root, text="1/4", state = 'disabled', \
          command = lambda: self.quarter(1), width = 5, height = 3, bd = 3, \
          bg = btcolor1, activebackground = btcolor2)
        self.bt_quarter.pack()
        self.bt_quarter.place(relx=(bet_b_x + btw_bet_b*3)/table_width, \
                           rely=bet_b_y/table_height)

        # half button
        self.bt_half = Button(root, text="1/2", state = 'disabled', \
          command = lambda: self.half(1), width = 5, height = 3, bd = 3, \
          bg = btcolor1, activebackground = btcolor2)
        self.bt_half.pack()
        self.bt_half.place(relx=(bet_b_x + btw_bet_b*4)/table_width, \
                           rely=bet_b_y/table_height)

        # full button
        self.bt_full = Button(root, text="Full", state = 'disabled', \
          command = lambda: self.full(1), width = 5, height = 3, bd = 3, \
          bg = btcolor1, activebackground = btcolor2)
        self.bt_full.pack()
        self.bt_full.place(relx=(bet_b_x + btw_bet_b*5)/table_width, \
                           rely=bet_b_y/table_height)

        # ddadang button
        self.bt_ddadang = Button(root, text="X2", state = 'disabled', \
          command = lambda: self.ddadang(1), width = 5, height = 3, bd = 3, \
          bg = btcolor1, activebackground = btcolor2)
        self.bt_ddadang.pack()
        self.bt_ddadang.place(relx=(bet_b_x + btw_bet_b*6)/table_width, \
                              rely=bet_b_y/table_height)

        # manual betting
        self.var_manual = IntVar()
        self.scale = Scale(root, from_=0, to = self.getBetlimit(),
          resolution = 50, tickinterval = self.getBetlimit(), \
          variable = self.var_manual, orient = HORIZONTAL, \
          length = 110, bd=0, relief = 'groove', bg = btcolor1, \
          troughcolor = btcolor1)
        self.scale.pack()
        self.scale.place(relx=(bet_b_x + btw_bet_b*7.2)/table_width, \
                              rely=bet_b_y/table_height)
        self.bt_manual = Button(root, text="Manual", state = 'disabled', \
          command = lambda: self.manual(1), width = 6, height = 3, bd = 3, \
          bg = btcolor1, activebackground = btcolor2)
        self.bt_manual.pack()
        self.bt_manual.place(relx=(bet_b_x + btw_bet_b*9.6)/table_width, \
                              rely=bet_b_y/table_height)


    def show_chips(self):
        # 칩표시 관련 위치정보
        btw_chips_x = 30 + 4 # 칩 사이의 가로 간격(안 겹치려면 50 이상)
        btw_chips_y = 3      # 칩 사이의 세로 간격(3~5 픽셀이 적당)
        chip_x = []
        chip_x.append(300)  # 베팅된 칩의 배치가 시작되는 x좌표값
        chip_x.append(40)   # 플레이어의 칩 배치가 시작되는 x좌표값
        chip_x.append(40)   # 컴퓨터의 칩 배치가 시작되는 x좌표값
        chip_y = []
        chip_y.append(265)                       # 베팅된 칩의 배치가 시작되는 y좌표값
        chip_y.append(card_start_height_p1 + 75) # 플레이어의 칩 배치가 시작되는 y좌표값
        chip_y.append(card_start_height_p2 + 75) # 컴퓨터의 칩 배치가 시작되는 y좌표값

        # 보유 금액에 맞춰 칩 갯수 지정
        for x in range(0,3):
            amount = self.money[x]
            temp_10000 = divmod(amount, 10000)[0]
            self.chips[x][0] = temp_10000
            rest = amount - temp_10000*10000
            temp_1000 = divmod(rest, 1000)[0]
            self.chips[x][1] = temp_1000
            rest = rest - temp_1000*1000
            temp_100 = divmod(rest, 100)[0]
            self.chips[x][2] = temp_100
            rest = rest - temp_100*100
            temp_10 = divmod(rest, 10)[0]
            self.chips[x][3] = temp_10
            rest = rest - temp_10*10
            self.chips[x][4] = rest

        # 기존에 그렸던 이미지와 텍스트를 삭제
        temp1 = len(self.chips_im)
        temp2 = len(self.chips_txt)
        if temp1 > 0:
            for x in range(0,temp1):
                canvas.delete(self.chips_im[temp1 - 1 - x])
                self.chips_im.pop()
            for x in range(0,temp2):
                canvas.delete(self.chips_txt[temp2 - 1 - x])
                self.chips_txt.pop()

        # 칩 이미지 및 갯수 텍스트 그리기
        for i in range(0, 3): # side 순서대로 반복
            for j in range(0, 5): # 비싼 칩 순서로 반복
                for k in range(0, self.chips[i][j]): # 칩 이미지 그리기
                    self.chips_im.append(canvas.create_image(\
                        chip_x[i] + btw_chips_x*j + random.randint(-2,2), \
                        chip_y[i] - btw_chips_y*k, image = self.chip_image[j]))
                if self.chips[i][j] != 0: # 칩 색깔별 갯수
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + btw_chips_x*j + 1, \
                        chip_y[i] - btw_chips_y*self.chips[i][j] - 15, \
                        anchor='center', fill='black', font=("Times", 15), \
                        text=self.chips[i][j]), )
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + btw_chips_x*j - 1, \
                        chip_y[i] - btw_chips_y*self.chips[i][j] - 15, \
                        anchor='center', fill='black', font=("Times", 15), \
                        text=self.chips[i][j]), )
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + btw_chips_x*j, \
                        chip_y[i] - btw_chips_y*self.chips[i][j] - 15 + 1, \
                        anchor='center', fill='black', font=("Times", 15), \
                        text=self.chips[i][j]), )
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + btw_chips_x*j, \
                        chip_y[i] - btw_chips_y*self.chips[i][j] - 15 - 1, \
                        anchor='center', fill='black', font=("Times", 15), \
                        text=self.chips[i][j]), )
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + btw_chips_x*j, \
                        chip_y[i] - btw_chips_y*self.chips[i][j] - 15, \
                        anchor='center', fill='white', font=("Times", 15), \
                        text=self.chips[i][j]), )

            if self.money[i] > 9: # 총 포커칩 포인트
                self.chips_txt.append(canvas.create_text(\
                    chip_x[i] + 40 + 1 , chip_y[i] + 40, \
                    anchor='w', fill='black', font=("Times", 15), \
                    text=self.money[i]))
                self.chips_txt.append(canvas.create_text(\
                    chip_x[i] + 40 - 1, chip_y[i] + 40, \
                    anchor='w', fill='black', font=("Times", 15), \
                    text=self.money[i]))
                self.chips_txt.append(canvas.create_text(\
                    chip_x[i] + 40, chip_y[i] + 40 + 1, \
                    anchor='w', fill='black', font=("Times", 15), \
                    text=self.money[i]))
                self.chips_txt.append(canvas.create_text(\
                    chip_x[i] + 40, chip_y[i] + 40 - 1, \
                    anchor='w', fill='black', font=("Times", 15), \
                    text=self.money[i]))
                self.chips_txt.append(canvas.create_text(\
                    chip_x[i] + 40, chip_y[i] + 40, \
                    anchor='w', fill='white', font=("Times", 15), \
                    text=self.money[i]))
        root.update()

        # 콜 하는데 필요한 칩 갯수 표시
        if max(0,self.money_betted[2]-self.money_betted[1]) != 0:
            self.chips_txt.append(canvas.create_text(500,270, \
                    anchor='w', fill='white', font=("Times", 15), \
                    text="Call: " + str(max(0,self.money_betted[2]-self.money_betted[1]))))
            root.update()

        # 내가 방금 베팅한 금액 표시
        if self.money_betted[1] > self.money_betted[2]:
            self.chips_txt.append(canvas.create_text(500,220, \
                    anchor='w', fill='white', font=("Times", 15), \
                    text="+ " + str(self.money_betted[1]-self.money_betted[2])))
        root.update()

    def bet_process(self, side = 1, num_of_given_card = 4):
        if num_of_given_card < 4:
            pass
        else: # 카드 4장 받았으면 베팅 시작!
            if side == 1: # 플레이어가 베팅하는 경우
                btcolor = 'orange'
                if self.betnum == 0: # 첫베팅(선)
                    if hasattr(bet, 'bettxt_p1'):
                        canvas.delete(self.bettxt_p1)
                    if hasattr(bet, 'bettxt_p2'):
                        canvas.delete(self.bettxt_p2)
                    self.show_message(0, "Your turn")
                    self.bt_die.config(state = 'active', bg = btcolor)
                    self.bt_check.config(state = 'active', bg = btcolor)
                    self.bt_quarter.config(state = 'active', bg = btcolor)
                    self.bt_half.config(state = 'active', bg = btcolor)
                    self.bt_full.config(state = 'active', bg = btcolor)
                    self.scale.config(bg = btcolor, troughcolor = 'Dark Orange')
                    self.bt_manual.config(state = 'active', bg = btcolor)
                elif self.betnum < 4:
                    if hasattr(bet, 'bettxt_p1'):
                        canvas.delete(self.bettxt_p1)
                    self.show_message(0, "Your turn")
                    self.bt_call.config(state = 'active', bg = 'green')
                    self.bt_die.config(state = 'active', bg = btcolor)
                    self.bt_quarter.config(state = 'active', bg = btcolor)
                    self.bt_half.config(state = 'active', bg = btcolor)
                    self.bt_full.config(state = 'active', bg = btcolor)
                    self.bt_ddadang.config(state = 'active', bg = btcolor)
                    self.scale.config(bg = btcolor, troughcolor = 'Dark Orange')
                    self.bt_manual.config(state = 'active', bg = btcolor)
                else: # 이미 네 번의 레이즈가 모두 끝난 경우
                    canvas.delete(self.bettxt_p1)
                    self.show_message(0, "No more raise")
                    self.show_message(0, "Your turn, Call or Fold?")
                    self.bt_call.config(state = 'active', bg = 'green')
                    self.bt_die.config(state = 'active', bg = btcolor)
            else: # 컴퓨터가 베팅하는 경우
                bet_list = []
                generator = self.botStrategy()
                # 첫 베팅인 경우에는 Fold 하지 않는 것으로 설정
                if len(p1_cards) == 4:
                    generator[0] = 0
                if self.betnum == 0: # 선베팅 - 콜(1)&따당(6) 불가능
                    if hasattr(bet, 'bettxt_p1'):
                        canvas.delete(self.bettxt_p1)
                    if hasattr(bet, 'bettxt_p2'):
                        canvas.delete(self.bettxt_p2)
                    generator[1] = 0
                    generator[6] = 0
                    for i in range(0,7):
                        for j in range(generator[i]):
                            bet_list.append(i)
                elif self.betnum < 4: # 선베팅이 아닌 경우 - 체크(2) 불가능
                    if hasattr(bet, 'bettxt_p2'):
                        canvas.delete(self.bettxt_p2)
                    generator[2] = 0
                    for i in range(0,7):
                        for j in range(generator[i]):
                            bet_list.append(i)
                else: # 이미 네 번의 레이즈가 모두 끝남 - 다이(0)&콜(1)만 가능
                    canvas.delete(self.bettxt_p2)
                    for x in range(2,7):
                        generator[1] = generator[1] + generator[x]
                        generator[x] = 0
                    for i in range(0,7):
                        for j in range(generator[i]):
                            bet_list.append(i)
                random.shuffle(bet_list)

                # test code start
                # print(generator)
                # print("1.Fold:    %.2f%%" % float(bet_list.count(0)*100/len(bet_list)))
                # print("2.Call:    %.2f%%" % float(bet_list.count(1)*100/len(bet_list)))
                # print("3.Check:   %.2f%%" % float(bet_list.count(2)*100/len(bet_list)))
                # print("4.Quarter: %.2f%%" % float(bet_list.count(3)*100/len(bet_list)))
                # print("5.Half:    %.2f%%" % float(bet_list.count(4)*100/len(bet_list)))
                # print("6.Full:    %.2f%%" % float(bet_list.count(5)*100/len(bet_list)))
                # print("7.Double:  %.2f%%" % float(bet_list.count(6)*100/len(bet_list)))
                # print("Choice = %s" % str(bet_list[0]+1))
                # test code end

                if bet_list[0] == 0:
                    self.die(2)
                elif bet_list[0] == 1:
                    self.call(2)
                elif bet_list[0] == 2:
                    self.check(2)
                elif bet_list[0] == 3:
                    self.quarter(2)
                elif bet_list[0] == 4:
                    self.half(2)
                elif bet_list[0] == 5:
                    self.full(2)
                elif bet_list[0] == 6:
                    self.ddadang(2)

    def botStrategy(self, version = 1):
        p1_hands = copy.deepcopy(p1_cards)
        p2_hands = copy.deepcopy(p2_cards)
        # computer knows only opened cards, not hidden cards of player.
        del p1_hands[0:2]
        if len(p1_hands) == 5:
            del p1_hands[-1] # delete last hidden card

        if version == 1: # simple strategy using rank ratio
            rank1 = get_rank(p1_hands)[0]
            rank2 = get_rank(p2_hands)[0]
            rank_ratio = (rank1 - rank2)/300 # -199 ~ 199 (Bigger is better)
            stragety = [1000]
            for x in range(0,6):
                stragety.append(max(1,int(stragety[-1]*(1+rank_ratio))))
            # 이기고 있으면 최소한 Fold는 하지 않게 설정
            if rank1 > rank2:
                stragety[0] = 0

        elif version == 2: # strategy using simulation
            pass

        elif version == 3: # 플레이어 베팅 패턴 학습전략
            pass

        return stragety

    def bet_money(self, side_from = 0, amount=0):
        self.money[side_from] -= amount
        self.money[0] += amount
        self.money_betted[side_from] += amount
        self.show_chips()

    def close_money(self):
        global who_wins
        if who_wins[0][-1] == 1:
            self.money[1] += self.money[0]
        elif who_wins[0][-1] == 2:
            self.money[2] += self.money[0]
        else:
            self.money[1] += int(self.money[0]/2)
            self.money[2] += int(self.money[0]/2)
        self.money[0] = 0
        self.show_chips()
        self.scale.config(to=self.getBetlimit())
        root.after(1500, setNextGame())

    def disabling_all(self):
        btcolor = 'Dim Gray'
        self.bt_die.config(state = 'disabled', bg = btcolor)
        self.bt_call.config(state = 'disabled', bg = btcolor)
        self.bt_check.config(state = 'disabled', bg = btcolor)
        self.bt_quarter.config(state = 'disabled', bg = btcolor)
        self.bt_half.config(state = 'disabled', bg = btcolor)
        self.bt_full.config(state = 'disabled', bg = btcolor)
        self.bt_ddadang.config(state = 'disabled', bg = btcolor)
        self.scale.config(bg = btcolor, troughcolor = btcolor)
        self.bt_manual.config(state = 'disabled', bg = btcolor)

    def die(self, side = 0):
        self.disabling_all()
        self.betnum = 0 # 레이즈 횟수 리셋
        who_wins[0].append(self.get_op_side(side))
        self.show_message(side, "Fold")
        self.money_betted = [0,0,0]
        self.close_money()

    def call(self, side = 0):
        amount = max(0, self.money_betted[self.get_op_side(side)] \
                                 - self.money_betted[side])
        if amount > self.money[side]:
            if side == 1:
                self.show_message(0, 'Short of money!!')
            else:
                self.money[2] += 100000
                self.show_chips()
                self.bet_process(2, len(p1_cards))
        else:
            self.disabling_all()
            self.bet_money(side, amount)
            self.show_message(side, "Call")
            self.betnum = 0 # 레이즈 횟수 리셋
            get_more_card()

    def check(self, side = 0):
        amount = self.base_bet
        if amount > self.money[side]:
            if side == 1:
                self.show_message(0, 'Short of money!!')
            else:
                self.money[2] += 100000
                self.check(2)
        else:
            self.disabling_all()
            if len(p1_cards) != 3: # 기본베팅이 아닌 경우에만
                self.betnum += 1   # 레이즈 1회 추가
                self.show_message(side, "Check")
            self.bet_money(side, self.base_bet)
            self.bet_process(self.get_op_side(side), len(p1_cards))

    def quarter(self, side = 0):
        amount = max(0, self.money_betted[self.get_op_side(side)] \
                                 - self.money_betted[side])
        amount = int(self.money[0] + amount)/4
        if amount > self.money[side]:
            if side == 1:
                self.show_message(0, 'Short of money!!')
            else:
                self.bet_process(2, len(p1_cards))
        else:
            self.disabling_all()
            self.betnum += 1 # 레이즈 1회 추가
            self.bet_money(side, max(0, self.money_betted[self.get_op_side(side)] \
                                     - self.money_betted[side]))
            self.bet_money(side,max(0, int(self.money[0]/4)))
            self.show_message(side, "Quarter")
            self.bet_process(self.get_op_side(side), len(p1_cards))

    def half(self, side = 0):
        amount = max(0, self.money_betted[self.get_op_side(side)] \
                                 - self.money_betted[side])
        amount = int(self.money[0] + amount)/2
        if amount > self.money[side]:
            if side == 1:
                self.show_message(0, 'Short of money!!')
            else:
                self.bet_process(2, len(p1_cards))
        else:
            self.disabling_all()
            self.betnum += 1 # 레이즈 1회 추가
            self.bet_money(side, max(0, self.money_betted[self.get_op_side(side)] \
                                     - self.money_betted[side]))
            self.bet_money(side,max(0, int(self.money[0]/2)))
            self.show_message(side, "Half")
            self.bet_process(self.get_op_side(side), len(p1_cards))

    def full(self, side = 0):
        amount = max(0, self.money_betted[self.get_op_side(side)] \
                                 - self.money_betted[side])
        amount = (self.money[0] + amount)*2
        if amount > self.money[side]:
            if side == 1:
                self.show_message(0, 'Short of money!!')
            else:
                self.bet_process(2, len(p1_cards))
        else:
            self.disabling_all()
            self.betnum += 1 # 레이즈 1회 추가
            self.bet_money(side, max(0, self.money_betted[self.get_op_side(side)] \
                                     - self.money_betted[side]))
            self.bet_money(side, max(0, self.money[0]))
            self.show_message(side, "Full")
            self.bet_process(self.get_op_side(side), len(p1_cards))

    def ddadang(self, side = 0):
        amount = max(0, (self.money_betted[self.get_op_side(side)] \
                                     - self.money_betted[side])*2)
        if amount > self.money[side]:
            if side == 1:
                self.show_message(0, 'Short of money!!')
            else:
                self.bet_process(2, len(p1_cards))
        else:
            self.disabling_all()
            self.betnum += 1 # 레이즈 1회 추가
            self.bet_money(side, amount)
            self.show_message(side, "Double")
            self.bet_process(self.get_op_side(side), len(p1_cards))

    def manual(self, side = 0):
        amount = max(0, self.money_betted[self.get_op_side(side)] \
                                 - self.money_betted[side])
        amount = amount + self.var_manual.get()
        if amount > self.money[side]:
            if side == 1:
                self.show_message(0, 'Short of money!!')
            else:
                self.bet_process(2, len(p1_cards))
        else:
            self.disabling_all()
            self.betnum += 1 # 레이즈 1회 추가
            self.bet_money(side, amount)
            self.show_message(side, str(amount))
            self.bet_process(self.get_op_side(side), len(p1_cards))

    def get_op_side(self, side = 1):
        if side == 1:   return 2
        elif side == 2: return 1

def setNextGame():
    global next_game
    next_game = True

def getNextGame():
    if not next_game:
        return True
    else:
        return False

def updating_root():
    root.update_idletasks()
    root.update()

class Menu_contents():
    def __init__(self):
        self.im_pokerhands = PhotoImage(file=relpath('resource\\poker_hands.gif'))
        self.im_pokerbot = PhotoImage(file=relpath('resource\\pokerbot.gif'))
        self.im_Teaminfinite = PhotoImage(file=relpath('resource\\Team_infinite_50.gif'))
        self.nickname = ""
        self.E1 = 0
        self.var = IntVar()
        self.R = []

    # ranking server plan
    # DB에 저장할 자료: nickname, money, level, 저장시간

    def load(self):
        try:
            with open('save.pkl', 'rb') as f:
                self.unpickled_file = pickle.load(f)
                if len(self.unpickled_file) > 10: # 최근 10개만 남기고 기록 삭제
                    while len(self.unpickled_file) > 10:
                        self.unpickled_file.pop(0)
            self.popup_load = Toplevel()
            self.popup_load.title("Load")
            self.popup_load.resizable(0,0)
            self.popup_load.attributes("-topmost",1, "-toolwindow", 1)

            # 제목행
            Label(self.popup_load, text = "Choice")\
                .grid(row=0, column=0, padx = 5, pady = 5)
            Label(self.popup_load, text = "User Name")\
                .grid(row=0, column=1, padx = 5, pady = 5)
            Label(self.popup_load, text = "Chips")\
                .grid(row=0, column=2, padx = 5, pady = 5)
            Label(self.popup_load, text = "Save time")\
                .grid(row=0, column=3, padx = 5, pady = 5)

            # 내용
            num = len(self.unpickled_file) # number of saved records
            for x in range(0, num):
                self.R.append(Radiobutton(self.popup_load, variable = self.var, value = x))
                self.R[-1].grid(row = num-x, column = 0, padx = 5, pady = 5)
                Label(self.popup_load, text = self.unpickled_file[x]['nickname'])\
                    .grid(row = num-x, column=1, padx = 5, pady = 5)
                Label(self.popup_load, text = self.unpickled_file[x]['money'])\
                    .grid(row = num-x, column=2, padx = 5, pady = 5)
                Label(self.popup_load, text = str(self.unpickled_file[x]['time']))\
                    .grid(row = num-x, column=3, sticky = "w", padx = 5, pady = 5)
            Button(self.popup_load, text = "Load", width = 8, height = num*2+1, \
            command = self.getCheck).\
            grid(row=0, column=4, rowspan=num+1, padx = 5, pady = 5)
            self.R[-1].select()
        except:
            messagebox.showinfo("Load", "No save file")

    def getCheck(self):
        self.nickname =self.unpickled_file[self.var.get()]['nickname']
        bet.money[1] = self.unpickled_file[self.var.get()]['money']
        messagebox.showinfo("Load", "Load successfully")
        self.popup_load.destroy()
        bet.show_chips()

    def save(self):
        self.popup_save = Toplevel()
        self.popup_save.title("Save")
        self.popup_save.resizable(0,0)
        self.popup_save.attributes("-topmost",1, "-toolwindow", 1)
        Label(self.popup_save, text = "User Name").\
        grid(row=0, column=0, sticky = "w", padx = 5, pady = 5)
        self.E1 = Entry(self.popup_save, bd=4)
        self.E1.grid(row=0, column=1, sticky = "e", padx = 5, pady = 5)
        Label(self.popup_save, text = "Gethered Chips: ").\
        grid(row=1, column=0, sticky = "w", padx = 5, pady = 5)
        Label(self.popup_save, text = bet.money[1]).\
        grid(row=1, column=1, sticky = "e", padx = 5, pady = 5)
        Button(self.popup_save, text = "Save", width = 8, height = 4, \
        command = self.getText).\
        grid(row=0, column=2, rowspan=2, padx = 5, pady = 5)
        self.E1.focus()
        self.popup_save.bind("<Return>", lambda event: self.getText())

    def getText(self):
        self.nickname = self.E1.get()
        if self.nickname == "":
            messagebox.showinfo("Error", "Input your nickname")
        elif self.nickname.count(':') > 0 or self.nickname.count(',') > 0:
            messagebox.showinfo("Error", "nickname can't include \':\' or \',\'.")
        else:
            # local save
            unpickled_file = []
            try:
                with open('save.pkl', 'rb') as f:
                    unpickled_file += pickle.load(f)
            except:
                pass
            with open('save.pkl', 'wb') as f:
                new_data = {'nickname': self.nickname, 'money': bet.money[1], \
                'time': str(datetime.now()).split()[0]}
                unpickled_file.append(new_data)
                pickle.dump(unpickled_file, f)

            # world ranking save
            url = "http://nickado.cafe24.com/rank.php?action=set&name=" \
                + str(self.nickname) +"&score=" + str(bet.money[1])
            urllib.request.urlopen(url)

            # success message
            messagebox.showinfo("Save", "Save successfully")
            self.popup_save.destroy()

    def poker_hands(self): # 완료
        self.popup_pokerhands = Toplevel()
        self.popup_pokerhands.title("Poker hands")
        self.popup_pokerhands.resizable(0,0)
        self.popup_pokerhands.attributes("-topmost",1, "-toolwindow", 1)
        self.canvas_pokerhands = Canvas(self.popup_pokerhands, width=500, \
        height=718, bd=0)
        self.canvas_pokerhands.pack()
        self.canvas_pokerhands.create_image(0,0, anchor=NW, image=self.im_pokerhands)

    def betting(self):
        self.popup_betting = Toplevel()
        self.popup_betting.title("Betting")
        self.popup_betting.resizable(0,0)
        self.popup_betting.attributes("-topmost",1, "-toolwindow", 1)

        # show subject line
        Label(self.popup_betting, text = "Types of Bets")\
        .grid(row=0, column=0, padx = 5, pady = 5, ipadx = 5)
        Label(self.popup_betting, \
        text = "Decription")\
        .grid(row=0, column=1, padx = 5, pady = 5, ipadx = 5)

        # show split bar
        Label(self.popup_betting, \
        text = "-----------------").grid(row=1, column=0, padx = 5, pady = 0, ipadx = 5)
        Label(self.popup_betting, \
        text = "-------------------------------------------------------------------")\
        .grid(row=1, column=1, padx = 5, pady = 0, ipadx = 5)

        # Call
        Label(self.popup_betting, \
        text = "Call").grid(row=2, column=0, padx = 5, pady = 5, ipadx = 5)
        Label(self.popup_betting, \
        text = "To bet as much as Poker bot raised just before")\
        .grid(row=2, column=1, padx = 5, pady = 5, ipadx = 5)

        # Fold
        Label(self.popup_betting, \
        text = "Fold").grid(row=3, column=0, padx = 5, pady = 5, ipadx = 5)
        Label(self.popup_betting, \
        text = "To discard one's hand and forfeit interest in the current pot")\
        .grid(row=3, column=1, padx = 5, pady = 5, ipadx = 5)

        # Check
        Label(self.popup_betting, \
        text = "Check").grid(row=4, column=0, padx = 5, pady = 5, ipadx = 5)
        Label(self.popup_betting, \
        text = "To bet as much as minimum amount(2 Chips)")\
        .grid(row=4, column=1, padx = 5, pady = 5, ipadx = 5)

        # Quarter
        Label(self.popup_betting, \
        text = "Quarter").grid(row=5, column=0, padx = 5, pady = 5, ipadx = 5)
        Label(self.popup_betting, \
        text = "Call + To bet 25% of pot")\
        .grid(row=5, column=1, padx = 5, pady = 5, ipadx = 5)

        # Half
        Label(self.popup_betting, \
        text = "Half").grid(row=6, column=0, padx = 5, pady = 5, ipadx = 5)
        Label(self.popup_betting, \
        text = "Call + To bet 50% of pot")\
        .grid(row=6, column=1, padx = 5, pady = 5, ipadx = 5)

        # Full
        Label(self.popup_betting, \
        text = "Full").grid(row=7, column=0, padx = 5, pady = 5, ipadx = 5)
        Label(self.popup_betting, \
        text = "Call + To bet 100% of pot")\
        .grid(row=7, column=1, padx = 5, pady = 5, ipadx = 5)

        # Double
        Label(self.popup_betting, \
        text = "Double").grid(row=8, column=0, padx = 5, pady = 5, ipadx = 5)
        Label(self.popup_betting, \
        text = "To bet twice as much as 'Call'")\
        .grid(row=8, column=1, padx = 5, pady = 5, ipadx = 5)

        # Manual
        Label(self.popup_betting, \
        text = "Manual").grid(row=9, column=0, padx = 5, pady = 5, ipadx = 5)
        Label(self.popup_betting, \
        text = "Call + To bet as much as one wants(limited by player's level")\
        .grid(row=9, column=1, padx = 5, pady = 5, ipadx = 5)

    def poker_bot(self): # 완료
        self.popup_pokerbot = Toplevel()
        self.popup_pokerbot.title("Poker bot is...")
        self.popup_pokerbot.resizable(0,0)
        self.popup_pokerbot.attributes("-topmost",1, "-toolwindow", 1)
        self.canvas_pokerbot = Canvas(self.popup_pokerbot, width=400, height=200, bd=0)
        self.canvas_pokerbot.pack()
        self.canvas_pokerbot.create_image(10,10, anchor=NW, \
        image=self.im_pokerbot)
        self.canvas_pokerbot.create_text(10, 120, anchor=NW, \
        text="Poker bot can't read your hidden cards in this program.")
        self.canvas_pokerbot.create_text(10, 140, anchor=NW, \
        text="He computes the probability of winning and applies it for betting.")
        self.canvas_pokerbot.create_text(10, 160, anchor=NW, \
        text="He will be upgraded continually.")

    def about(self): # 완료
        self.popup_about = Toplevel()
        self.popup_about.title("Development Info")
        self.popup_about.resizable(0,0)
        self.popup_about.attributes("-topmost",1, "-toolwindow", 1)
        self.canvas_about = Canvas(self.popup_about, width=300, height=100, bd=0)
        self.canvas_about.pack()
        self.canvas_about.create_image(10,30, anchor=NW, \
        image=self.im_Teaminfinite)
        self.canvas_about.create_text(70, 30, anchor=NW, \
        text="- Version: 1.1")
        self.canvas_about.create_text(70, 50, anchor=NW, \
        text="- Team Infinite. All rights reserved.")
        self.canvas_about.create_text(70, 70, anchor=NW, \
        text="- Bug report: teaminfinite83@gmail.com")

# 기본적인 윈도우 크기 및 수치 설정
table_width=800
table_height=500
card_width=71
card_height=96
between_cards = card_width - 10
card_start_width_p1 = 200
card_start_width_p2 = card_start_width_p1 + between_cards*6
card_start_height_p1 = 330
card_start_height_p2 = 50

# 윈도우 창 띄우기
root=Tk()
root.title("GoPoker")
root.resizable(0,0)
canvas=Canvas(root, width = table_width, height = table_height,\
              bd=0, highlightthickness=0)
canvas.pack()

# 메뉴바
menubar = Menu(root)
contents = Menu_contents()
gamemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Record", menu=gamemenu)
gamemenu.add_command(label="Load", command=contents.load)
gamemenu.add_command(label="Save", command=contents.save)
gamemenu.add_separator()
gamemenu.add_command(label="Exit", command=root.destroy)

helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="Poker hands", command=contents.poker_hands)
helpmenu.add_command(label="Betting", command=contents.betting)

infomenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Info", menu=infomenu)
infomenu.add_command(label="Poker bot is...", command=contents.poker_bot)
infomenu.add_command(label="About...", command=contents.about)

root.config(menu=menubar)

# 베팅 및 게임칩, 게임머니 관련 객체 생성
bet = Bet()

# halo effect를 위한 이미지 로드
halo_1_im = PhotoImage(file=relpath('resource\\halo_1.gif'))
halo_2_im = PhotoImage(file=relpath('resource\\halo_2.gif'))

# 누가 이겼는지를 기록하는 리스트(0:비김, 1:플레이어, 2:컴퓨터)
# [0]은 이전 판의 승부, [1]은 게임 중의 오픈된 카드 패의 족보 기준 승패
who_wins = [[1],[1]] # 초기 값은 플레이어가 이전 판을 이긴 것처럼(선으로) 설정함

# 한 판의 게임을 반복하는 main loop
while True:
    # 한 판의 게임이 끝나면 모든 위젯과 이미지를 지우게 되므로 배경도 다시 그려야 함
    background = PhotoImage(file=relpath('resource\\table.gif'))
    bg = canvas.create_image(0,0, anchor=NW, image=background)
    root.update()

    # 게임머니 보여주기
    bet.show_chips()

    # 다음 게임으로 넘어가기 여부를 판단하는 변수
    next_game = False

    # 한 벌의 카드를 생성
    # 1(에이스)부터 13(킹)까지 spade, diamond, clover, heart 순으로 배열
    # 무늬별 카드 장수가 13장이므로, 13으로 나눈 몫이 1이면 spade, 2이면 diamond,
    # 3이면 clover, 4이면 heart임. 13으로 나눈 나머지(0인 경우 13)가 카드의 숫자가 됨
    deck=list(range(1,53))
    card_images=[]
    for x in deck:
        card_images.append(PhotoImage(file=relpath(image_path(x))))
    b1fv_image=PhotoImage(file=relpath('resource\\b1fv.gif'))
    random.shuffle(deck)
    deck_image = [] # 덱표시(뒷장)에 사용될 전역변수 생성
    deck_place = [] # 덱 이미지(뒷장)의 x좌표값을 기록하는 전역변수 생성
    show_deck()

    # Player1과 상대편에게 첫 카드 3장씩을 배정하고 배정된 카드는 덱에서 제외
    if who_wins[0][-1] == 1: # 이전 판에 플레이어가 이겼을 경우
        p1_cards=deck[0:3]
        del deck[0:3]
        p2_cards=deck[0:3]
        del deck[0:3]
    else:
        p2_cards=deck[0:3]
        del deck[0:3]
        p1_cards=deck[0:3]
        del deck[0:3]

    # Player2의 카드 중 오픈할 카드를 맨 뒤로 정렬
    a=open_which_card()
    b=p2_cards[a]
    del p2_cards[a]
    p2_cards.append(b)

    # 슬롯을 생성한다
    p1_slot=[]
    p2_slot=[]

    # 첫 3장의 카드를 보여준다
    if who_wins[0][-1] == 1: # 이전 판에 플레이어가 이겼을 경우
        show_cards_p1()
        show_cards_p2()
    else:
        show_cards_p2()
        show_cards_p1()

    # Player1의 카드(버튼)에 각각의 이벤트 함수를 대응시킨다
    p1_slot[0].config(command = f1, activebackground = 'yellow')
    p1_slot[1].config(command = f2, activebackground = 'yellow')
    p1_slot[2].config(command = f3, activebackground = 'yellow')

    # 기본베팅
    bet.check(1)
    bet.check(2)

    # 오픈 안내멘트와 halo effect 동시 구현을 위한 multithreading
    threads = []
    threads.append(threading.Thread(target=bet.show_message(0, \
      "Choose one card to be opened")))
    threads.append(threading.Thread(target=show_halo()))
    threads[0].start()
    threads[1].start()
    for th in threads:
        th.join()

    # 화면을 계속해서 업데이트 해주는 sub loop
    while getNextGame():
        try:
            root.after(5, updating_root())
        except:
            quit()

    # 버튼들은 일일이 destroy 해야 자국이 남지 않고 사라짐
    for x in range(0,len(p1_slot)):
        p1_slot[x].destroy()

    # p2의 카드를 화면에서 지워줌
    canvas.delete(p2_slot)
    # 참고로 승패 코멘트는 배경을 다시 뿌리면서 자동적으로 묻혀짐

    continue # 다시 main while loop의 처음으로 돌아감
