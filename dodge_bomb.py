import os
import sys
import random
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {  #移動量辞書
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT:(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect) -> tuple[bool,bool]:
    """
    引数:こうかとんRectかばくだんRect
    戻り値:タプル(横方向判定結果,縦方向判定結果)
    画面外ならTrue,画面外ならFalse
    """
    yoko,tate = True, True  #初期値:画面の中
    if rct.left < 0 or WIDTH < rct.right:  #横方向の画面外判定
        yoko = False
    if rct.top < 0 or HEIGHT <rct.bottom:  #縦方向の画面外判定
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:  #ゲームオーバー画面
    go_img = pg.Surface((WIDTH,HEIGHT))  #黒画面
    pg.draw.rect(go_img,(0,0,0),(0,0,400,300))
    go_img.set_alpha(128)
    kc_img = pg.image.load("fig/8.png")  #こうかとん画像
    fonto = pg.font.Font(None,80)  #コメント
    txt = fonto.render("Game Over",True,(255,255,255))
    screen.blit(go_img,[0,0])
    screen.blit(txt,[400,300])
    screen.blit(kc_img,[350,300])
    screen.blit(kc_img,[725,300])
    pg.display.update()


def init_bb_imgs() -> tuple[list[pg.Surface],list[int]]:  #爆弾の拡大、加速
    bb_accs = [a for a in range(1,11)]  #加速
    bb_imgs=[]  #拡大
    for r in range(1,11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
        bb_img.set_colorkey((0,0,0))
        bb_imgs.append(bb_img)
    return bb_imgs,bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    bb_imgs, bb_accs = init_bb_imgs()  
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    tmr = 0
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0,WIDTH)
    bb_rct.centery = random.randint(0,HEIGHT)
    clock = pg.time.Clock()
    vx,vy = +5,+5  #爆弾の移動速度
    while True:
        bb_img = bb_imgs[min(tmr//500,9)]
        avx = vx*bb_accs[min(tmr//500,9)]
        avy = vy*bb_accs[min(tmr//500,9)]

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            time.sleep(5)
            return
        
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  #移動をなかったことにする
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx,avy)  #爆弾の移動
        yoko,tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
