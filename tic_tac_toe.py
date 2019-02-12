# tic_tac_toe by opencv

from numpy import shape as np_shape
from numpy import array as np_array
from numpy import zeros as np_zeros
from numpy import ones as np_ones
from numpy import sum as np_sum
from numpy import isin as np_isin
from cv2 import line as cv2_line
from cv2 import putText as cv2_putText
from cv2 import imshow as cv2_imshow
from cv2 import imwrite as cv2_imwrite
from cv2 import waitKey as cv2_waitKey
from cv2 import destroyAllWindows as cv2_destroyAllWindows
from cv2 import FONT_HERSHEY_SIMPLEX as cv2_FONT_HERSHEY_SIMPLEX

def lines(ground,dim_x,dim_y):
    d_small = 60
    d_long = 3*d_small 
    x_c,y_c = dim_x/2,dim_y/2
    points = np_array([[y_c-d_small,x_c-d_long],[y_c-d_small,x_c+d_long],
                      [y_c+d_small,x_c-d_long],[y_c+d_small,x_c+d_long],
                      [y_c+d_long,x_c-d_small],[y_c-d_long,x_c-d_small],
                      [y_c-d_long,x_c+d_small],[y_c+d_long,x_c+d_small]])
    for j in xrange(np_shape(points)[0]/2):
        i = 2*j
        cv2_line(ground,(points[i,1],points[i,0]),(points[i+1,1],points[i+1,0]),[125,100,140],5)
    out = x_c,y_c,d_small,d_long
    return out

def center_points(out_lines):
    x_c,y_c,d_small,d_long = out_lines[0],out_lines[1],out_lines[2],out_lines[3]
    d = (d_small+d_long)/2+10
    x = [-1,0,1,-1,0,1,-1,0,1]
    y = [-1,-1,-1,0,0,0,1,1,1]
    out = np_zeros((len(x),3))
    out[:,0] = y
    out[:,1] = x
    out*=d
    out[:,0]+= y_c
    out[:,1]+= x_c
    out[:,-1] = -1
    out = out.astype('int32')
    return out

def fill_pose(ground,out_points,key,turn):
    if out_points[int(chr(key))-1,-1] == -1:
        out_points[int(chr(key))-1,-1] = int(chr(key))
        if turn == 0:
            s= "X"
        else:
            s = "O"
        ground[out_points[int(chr(key))-1,0]-25:out_points[int(chr(key))-1,0]+10,
                out_points[int(chr(key))-1,1]-20:out_points[int(chr(key))-1,1]+20,:]=255
        cv2_putText(ground,s,(out_points[int(chr(key))-1,1]-5,out_points[int(chr(key))-1,0]),cv2_FONT_HERSHEY_SIMPLEX,1,0)
        turn = 1-turn
    else:
        ground[dim_y-60:dim_y,20:dim_x,:]=255
        cv2_putText(ground,"Player "+str(turn+1),(30,dim_y-20),cv2_FONT_HERSHEY_SIMPLEX,0.5,0)
        cv2_putText(ground,"Number \""+chr(key)+"\" Is Already Taken",(30,dim_y-40),cv2_FONT_HERSHEY_SIMPLEX,0.5,[0,0,255])
    return turn

def winner(ground,turn,key,player_1=[],player_2=[]):
    win = [[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]
    if turn == 1:
        player_1.append(int(chr(key)))
        #player_1 = set(player_1)
    else:
        player_2.append(int(chr(key)))
        #player_2 = set(player_2)
    #print "p1",player_1
    j = 0
    for i in win:
        if np_sum(np_isin(list(set(player_2)),i)*1)==3:
            print "player 2 wins",i
            cv2_putText(ground,"Player 2 Wins",(40,40),cv2_FONT_HERSHEY_SIMPLEX,1,0)
            return 2
        elif np_sum(np_isin(list(set(player_1)),i)*1)==3:
            print "player 1 wins",i
            cv2_putText(ground,"Player 1 Wins",(40,40),cv2_FONT_HERSHEY_SIMPLEX,1,0)
            return 1
        elif np_sum(np_isin(list(set(player_1)),i)*1)>=1 and np_sum(np_isin(list(set(player_2)),i)*1)>=1:
            j+=1
        if (np_sum(np_isin(list(set(player_1)),i)*1)==2 or np_sum(np_isin(list(set(player_2)),i)*1)==2):
            print 'here'
    if j == 8:
        cv2_putText(ground,"No-One Wins",(40,40),cv2_FONT_HERSHEY_SIMPLEX,1,0)
        return 3
    return 0

def pause(time,ground):
    while time >= 1:
        ground[np_shape(ground)[1]/2+70:np_shape(ground)[1]/2+100,np_shape(ground)[1]/2-10:np_shape(ground)[1]/2+40,:]=255
        cv2_putText(ground,str(time),(np_shape(ground)[1]/2-5,np_shape(ground)[1]/2+93),cv2_FONT_HERSHEY_SIMPLEX,1,0)
        cv2_imshow("Tic_Tac_Toe",ground)
        k = cv2_waitKey(1000) & 0xFF
        if k == 27:
            return 1
        elif k!=255:
            return 0
        time-=1
    return 0
        
dim_y = 600
dim_x = int(dim_y * 1.618+0.5)
brk = 0
pl1,pl2=0,0
turn = 0 
while True:
    player_1=[]
    player_2=[]
    ground = np_ones((dim_y,dim_x,3))*255
    ground = ground.astype('uint8')

    out_lines = lines(ground,dim_x,dim_y)
    out_points =center_points(out_lines)

    for i in xrange(9):
        cv2_putText(ground,str(i+1),(out_points[i,1]-5,out_points[i,0]),cv2_FONT_HERSHEY_SIMPLEX,1,0)
    while True:
        cv2_imshow("Tic_Tac_Toe",ground)
        key = cv2_waitKey(1) & 0xFF
        if key == 27:
            brk = 1
            break
        elif key!=255:
            if key == 9:
                cv2_imwrite('tic_tac_toe.PNG', ground)
            if 49<=key<=57:
                turn = fill_pose(ground,out_points,key,turn)
                #cv2_imshow("Tic_Tac_Toe",ground)
                br = winner(ground,turn,key,player_1,player_2)
                cv2_imshow("Tic_Tac_Toe",ground)
                if br == 1 or br == 2:
                    pl1 += (br==1)*1
                    pl2 += (br==2)*1
                    turn = 1-turn
                    break
                if br == 3:
                    print "no one won"
                    break
            else:
                ground[dim_y-60:dim_y,20:dim_x,:]=255
                #cv2_putText(ground,"Player "+str(turn+1),(30,dim_y-20),cv2_FONT_HERSHEY_SIMPLEX,0.5,0)
                cv2_putText(ground,"Please Enter A Number between 1 and 9",(30,dim_y-40),cv2_FONT_HERSHEY_SIMPLEX,0.5,[0,0,255])

        ground[dim_y-30:dim_y,20:dim_x,:]=255
        cv2_putText(ground,"Turn: Player "+str(turn+1),(30,dim_y-20),cv2_FONT_HERSHEY_SIMPLEX,0.5,0)
        cv2_putText(ground,"Player 1: "+str(pl1),(30,100),cv2_FONT_HERSHEY_SIMPLEX,0.5,0)
        cv2_putText(ground,"Player 2: "+str(pl2),(30,130),cv2_FONT_HERSHEY_SIMPLEX,0.5,0)
        cv2_imshow("Tic_Tac_Toe",ground)

    ground[80:150,100:140,:]=255
    cv2_putText(ground,"Player 1: "+str(pl1),(30,100),cv2_FONT_HERSHEY_SIMPLEX,0.5,0)
    cv2_putText(ground,"Player 2: "+str(pl2),(30,130),cv2_FONT_HERSHEY_SIMPLEX,0.5,0)
    cv2_imshow("Tic_Tac_Toe",ground)
    if max(pl1,pl2)==3:
        if pl1>pl2:
            win = "1"
        else:
            win = "2"
        ground[:,:,:] = 255
        cv2_putText(ground,"Player 1: "+str(pl1),(30,100),cv2_FONT_HERSHEY_SIMPLEX,0.5,0)
        cv2_putText(ground,"Player 2: "+str(pl2),(30,130),cv2_FONT_HERSHEY_SIMPLEX,0.5,0)
        cv2_putText(ground,"Player "+win+" Wins",(dim_x/2-210,dim_y/2),cv2_FONT_HERSHEY_SIMPLEX,2,1)
        cv2_imshow("Tic_Tac_Toe",ground)
        pause(10,ground)
        break
    if brk == 1:
        break
    p = pause(10,ground)
    brk = p
    if brk == 1:
        break
cv2_destroyAllWindows()