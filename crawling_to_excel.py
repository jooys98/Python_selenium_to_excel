from selenium import webdriver

# 웹 자동화
from selenium.webdriver.common.by import By

# 요소를 찾기 위한 도구 <div class>
from selenium.webdriver.support.ui import WebDriverWait

# 페이지 로딩 대기
from selenium.webdriver.support import expected_conditions as EC

# 조건 체크
import time

# 시간 지연시 사용
import random

# 랜덤 대기 시간
import pandas as pd

# 파이썬 객체를 엑셀로 변환시켜주는 데이터 처리 라이브러리

driver = webdriver.Chrome()
# 크롬 드라이버 실행 / 접속
driver.get("https://linkkf.net/list/9/year/2018/")
# 정보를 긁어올 웹주소
time.sleep(random.uniform(5.0, 8.0))
# 봇 감지 방지를 위한 랜덤 대기 시간

try:
    articles = driver.find_elements(By.CLASS_NAME, "img-wrapper")
    # 애니메이션 목록에서 이미지 요소들 찾기
    article_data = []
    # 수집한 데이터 저장할 빈 리스트를 선언

    for article in articles[:15]:
        # 크롤링할 갯수
        try:
            driver.execute_script("arguments[0].click();", article)
            # 게시글 클릭
            time.sleep(3)

            WebDriverWait(driver, 13).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".detail-info-title.text-row-2")
                )
            )  # 페이지 로딩 대기

            try:
                # 필요한 정보 추출
                title = driver.find_element(
                    By.CSS_SELECTOR, ".detail-info-title.text-row-2"
                ).text
                company = driver.find_element(
                    By.XPATH, "/html/body/div[4]/div[2]/div/div[2]/div/ul/li[3]/a"
                ).text
                Round = driver.find_element(
                    By.XPATH, "/html/body/div[4]/div[2]/div/div[2]/div/ul/li[4]"
                ).text
                years = driver.find_element(
                    By.XPATH, "/html/body/div[4]/div[2]/div/div[2]/div/ul/li[5]/a"
                ).text

                #  태그가 없을 시 예외 처리 따로
                try:
                    tag1 = driver.find_element(
                        By.XPATH,
                        "/html/body/div[4]/div[2]/div/div[2]/div/ul/li[2]/a[1]",
                    ).text
                except:
                    tag1 = "태그 없음"

                try:
                    tag2 = driver.find_element(
                        By.XPATH,
                        "/html/body/div[4]/div[2]/div/div[2]/div/ul/li[2]/a[2]",
                    ).text
                except:
                    tag2 = "태그 없음"

                try:
                    tag3 = driver.find_element(
                        By.XPATH,
                        "/html/body/div[4]/div[2]/div/div[2]/div/ul/li[2]/a[3]",
                    ).text
                except:
                    tag3 = "태그 없음"

                image_url = driver.find_element(
                    By.CSS_SELECTOR, "img.lazyload"
                ).get_attribute("src")

                # 파이썬 객체 형태로 위에 선언한 배열에 값이 들어옴
                article_data.append(
                    {
                        "제목": title,
                        "제작사": company,
                        "횟수": Round,
                        "방영시기": years,
                        "태그1": tag1,
                        "태그2": tag2,
                        "태그3": tag3,
                        "이미지": image_url,
                    }
                )

            except Exception as e:
                print(f"데이터 수집 오류: {e}")
                driver.back()
                time.sleep(3)

        except Exception as e:
            print(f"페이지 처리 오류: {e}")
            driver.back()
            continue

    print(f"크롤링 완료. {len(article_data)}개 수집")
    # 수집한 데이터를 dataframe 으로 변환
    ys = pd.DataFrame(article_data)

    try:
        # 엑셀파일로 저장
        # 파일에 접근하여 정보를 업데이트
        existing_ys = pd.read_excel("aniwhere_data1.xlsx")
        updated_ys = pd.concat([existing_ys, ys], ignore_index=True)
        updated_ys.to_excel("aniwhere_data1.xlsx", index=False)
    except FileNotFoundError:
        df.to_excel("aniwhere_data1.xlsx", index=False)
# 파일이 없으면 새로 생성
except Exception as e:
    print(f"크롤링 오류: {e}")

finally:
    driver.quit()
