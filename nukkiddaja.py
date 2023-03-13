import sys
import numpy as np
import cv2 as cv


def erase_background(file_path):
    # 이미지 불러오기
    img = cv.imread(file_path)

    # 변환 graky
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # 임계값 조절
    mask = cv.threshold(gray, 250, 255, cv.THRESH_BINARY)[1]

    # mask
    mask = 255 - mask

    # morphology 적용
    # borderconstant 사용
    kernel = np.ones((3, 3), np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

    # anti-alias the mask
    # blur alpha channel
    mask = cv.GaussianBlur(mask, (0, 0), sigmaX=2, sigmaY=2, borderType=cv.BORDER_DEFAULT)

    # linear stretch so that 127.5 goes to 0, but 255 stays 255
    mask = (2 * (mask.astype(np.float32)) - 255.0).clip(0, 255).astype(np.uint8)

    # put mask into alpha channel
    result = img.copy()
    result = cv.cvtColor(result, cv.COLOR_BGR2BGRA)
    result[:, :, 3] = mask

    # 저장
    cv.imwrite(file_path + '_transparent.png', result)

    cv.imshow('Image', result)
    cv.waitKey()
    cv.destroyAllWindows()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("배경을 삭제하려고 하는 파일 경로를 인자로 넘겨주세요.")
    else:
        file_path = sys.argv[1]
        erase_background(file_path)
