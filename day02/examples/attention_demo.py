# -*- coding: utf-8 -*-
"""
01.Attention_v1.7.ipynb 전용 실행 모듈

비개발 직군 대상 실습에서 수강생이 읽을 필요가 없는 구현을
이야기 흐름에서 분리해 두기 위한 파일입니다. (강사·준비 담당자용)

노트북에서는 다음 세 가지만 호출합니다.

    준비()
    확인(긴메시지)
    비교(문맥A, 문맥B)

주의
----
* 화면에 출력되는 문구·그래프 라벨에는 기술 용어와 수치를 넣지 않습니다.
  (본 실습의 교육 목표가 알고리즘 구현이 아니라 '문맥에 따라 참고 위치가
   달라진다'는 관찰이기 때문입니다.)
* Attention 결과는 반드시 실제 학습된 모델의 출력에서 가져옵니다.
  보기 좋게 만들기 위해 값을 조작하거나 고정하지 않습니다.

동작 확인 환경 : Python 3.11.9 / TensorFlow 2.21.0 / Keras 3.15.1 / matplotlib 3.11.1
"""

import os

# 교육 화면을 덮는 환경 안내 로그만 정리합니다(실행 결과에는 영향이 없습니다).
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")

import logging
import random
import unicodedata
import warnings

import numpy as np

logging.getLogger("tensorflow").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=UserWarning, module="keras")

import tensorflow as tf  # noqa: E402

# TensorFlow 는 import 시점에 자체 logger 를 다시 설정하므로 여기서 한 번 더 낮춘다.
# (GPU 미사용 안내 등 실행 결과에 영향이 없는 환경 안내만 교육 화면에서 정리한다.)
tf.get_logger().setLevel(logging.ERROR)
logging.getLogger("tensorflow").setLevel(logging.ERROR)

import matplotlib  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

try:
    from absl import logging as _absl_logging

    _absl_logging.set_verbosity(_absl_logging.ERROR)
except Exception:  # pragma: no cover - absl 미설치 환경 대비
    pass


# ────────────────────────────────────────────────────────────────
# 한글 글꼴
# ────────────────────────────────────────────────────────────────
def _한글글꼴_설정():
    설치된글꼴 = {f.name for f in font_manager.fontManager.ttflist}
    for 후보 in ("Malgun Gothic", "Pretendard", "NanumGothic", "Noto Sans KR",
                 "AppleGothic", "Gulim"):
        if 후보 in 설치된글꼴:
            matplotlib.rcParams["font.family"] = 후보
            break
    matplotlib.rcParams["axes.unicode_minus"] = False
    return matplotlib.rcParams["font.family"]


_한글글꼴_설정()


# ────────────────────────────────────────────────────────────────
# 색상 (PPT 교안과 동일한 시각 문법: 진한 색 = 더 많이 참고)
# ────────────────────────────────────────────────────────────────
_강조색 = "#2E4F7C"
_흐린색 = "#D8D4CF"
_글자색 = "#201B18"
_보조색 = "#8A857F"

_SEED = 42

# ────────────────────────────────────────────────────────────────
# 예제 메시지 재료
# ────────────────────────────────────────────────────────────────
_구성품 = ["수신기", "충전기", "어댑터", "설명서", "거치대", "배터리", "스피커", "삼각대"]
_누락표현 = ["가 빠져 있었습니다", "가 들어 있지 않았습니다", "만 누락되어 있었습니다"]
_정상표현 = ["는 정상입니다", "도 잘 들어 있었습니다", "는 이상 없었습니다"]
_잡음문장 = [
    "지난주 노트북과 무선 마우스를 함께 주문했습니다",
    "택배는 어제 도착했습니다",
    "배송 기사님은 매우 친절했습니다",
    "영수증은 함께 들어 있었습니다",
    "결제는 카드로 정상 처리되었습니다",
]
_요청 = "이것만 다시 보내 주세요"

# 노트북에서 그대로 사용하는 시연 문장 -----------------------------------
긴메시지 = (
    "지난주 노트북과 무선 마우스를 함께 주문했습니다 택배는 어제 도착했습니다 "
    "배송 기사님은 매우 친절했습니다 충전기는 정상입니다 수신기가 빠져 있었습니다 "
    "영수증은 함께 들어 있었습니다 " + _요청
)

# 문맥 A / B — 구성품 등장 순서(수신기 · 충전기 · 설명서), 정상 표현("는 정상입니다"),
# 누락 표현("가 빠져 있었습니다"), 마지막 요청 문장을 모두 같게 두고
# '어느 구성품이 누락 상태인가'만 바꾼 비교 문장입니다.
# 두 문장 모두 11개 단어이며 마지막 네 단어가 완전히 같습니다.
문맥A = "수신기는 정상입니다 충전기는 정상입니다 설명서가 빠져 있었습니다 " + _요청
문맥B = "수신기가 빠져 있었습니다 충전기는 정상입니다 설명서는 정상입니다 " + _요청

_시연문장 = [긴메시지, 문맥A, 문맥B]

# 학습으로 채워지는 값 ---------------------------------------------------
_상태 = {"준비됨": False}


# ────────────────────────────────────────────────────────────────
# 준비 : 예제 메시지 생성 → 모델 구성 → 학습
# ────────────────────────────────────────────────────────────────
def 준비(조용히=False):
    """예제 메시지를 만들고 교육용 모델을 학습시킵니다. (수십 초 소요)"""
    random.seed(_SEED)
    tf.keras.utils.set_random_seed(_SEED)

    rng = random.Random(_SEED)
    모음 = {}
    while len(모음) < 400:
        등장구성품 = rng.sample(_구성품, rng.choice([2, 3, 4]))
        정답 = rng.choice(등장구성품)
        문장들 = rng.sample(_잡음문장, rng.choice([0, 1, 2]))
        for 부품 in 등장구성품:
            문장들.append(부품 + (rng.choice(_누락표현) if 부품 == 정답 else rng.choice(_정상표현)))
        rng.shuffle(문장들)
        메시지 = " ".join(문장들 + [_요청])
        if 메시지 not in _시연문장:          # 시연 문장은 연습에서 제외
            모음[메시지] = 정답

    메시지들 = list(모음.keys())
    정답들 = list(모음.values())
    경계 = 340

    최대길이 = max(len(m.split()) for m in 메시지들 + _시연문장)
    숫자화 = tf.keras.layers.TextVectorization(
        max_tokens=200, standardize=None, split="whitespace",
        output_sequence_length=최대길이,
    )
    숫자화.adapt(메시지들[:경계])
    사전 = 숫자화.get_vocabulary()

    입력 = 숫자화(메시지들).numpy()
    정답번호 = np.array([_구성품.index(a) for a in 정답들])

    폭 = 64
    문장입력 = tf.keras.Input(shape=(최대길이,), dtype="int32")
    표현 = tf.keras.layers.Embedding(len(사전), 폭, mask_zero=True)(문장입력)
    _, 마지막상태, _ = tf.keras.layers.LSTM(폭, return_state=True)(표현)
    질문 = tf.keras.layers.Reshape((1, 폭))(마지막상태)
    모은결과, 참고비중 = tf.keras.layers.Attention()(
        [질문, 표현, 표현], return_attention_scores=True
    )
    출력 = tf.keras.layers.Dense(len(_구성품), activation="softmax")(
        tf.keras.layers.Reshape((폭,))(모은결과)
    )

    모델 = tf.keras.Model(문장입력, 출력)
    모델.compile(optimizer="adam", loss="sparse_categorical_crossentropy",
                 metrics=["accuracy"])
    모델.fit(입력[:경계], 정답번호[:경계],
             validation_data=(입력[경계:], 정답번호[경계:]),
             epochs=40, batch_size=32, verbose=0)

    _상태.update(
        준비됨=True,
        숫자화=숫자화,
        사전=사전,
        관찰모델=tf.keras.Model(문장입력, [출력, 참고비중]),
        예시=메시지들[0],
    )

    if not 조용히:
        print("준비 완료")
        print("— 교육용으로 단순하게 만든 예제 메시지로 연습을 마쳤습니다.")
        print()
        print("연습에 사용한 메시지 예시")
        print("  " + _상태["예시"])
    return None


def _결과(문장):
    """실제 모델을 실행해 (예측 단어, 단어 목록, 참고 정도)를 돌려줍니다."""
    if not _상태["준비됨"]:
        raise RuntimeError("먼저 준비() 를 실행해 주세요.")
    번호 = _상태["숫자화"]([문장]).numpy()
    확률, 비중 = _상태["관찰모델"].predict(번호, verbose=0)
    단어들 = [_상태["사전"][t] for t in 번호[0] if t != 0]
    비중 = np.asarray(비중)[0, 0, : len(단어들)]
    예측 = _구성품[int(np.asarray(확률)[0].argmax())]
    return 예측, 단어들, 비중


# ────────────────────────────────────────────────────────────────
# 그림 그리기
# ────────────────────────────────────────────────────────────────
def _막대그리기(축, 단어들, 비중, 제목):
    최대 = int(np.argmax(비중))
    색 = [_강조색 if i == 최대 else _흐린색 for i in range(len(단어들))]
    축.bar(range(len(단어들)), 비중, color=색, width=0.62)
    축.set_xticks(range(len(단어들)))
    축.set_xticklabels(단어들, rotation=45, ha="right", fontsize=11, color=_글자색)
    축.set_yticks([])
    축.set_ylim(0, max(float(np.max(비중)) * 1.30, 1e-6))
    축.set_title(제목, fontsize=13.5, color=_글자색, pad=26)
    for 위치 in ("top", "right", "left"):
        축.spines[위치].set_visible(False)
    축.spines["bottom"].set_color(_흐린색)
    축.tick_params(axis="x", length=0)
    축.text(0.0, 1.02, "세로 길이 = 참고한 정도", transform=축.transAxes,
            fontsize=10, color=_보조색, ha="left", va="bottom")
    축.annotate("가장 많이 참고한 곳", xy=(최대, float(비중[최대])),
                xytext=(0, 9), textcoords="offset points",
                ha="center", fontsize=11, color=_강조색, fontweight="bold")


def _표시폭(글자열):
    """한글·한자는 두 칸을 차지하므로 실제 표시 폭을 센다."""
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
               for ch in 글자열)


def _글자막대(단어들, 비중, 개수=5):
    print("이번 계산에서 더 많이 참고한 곳")
    print()
    뽑은순서 = list(np.argsort(-비중)[:개수])
    최대폭 = max(_표시폭(단어들[i]) for i in 뽑은순서)
    for i in 뽑은순서:
        칸 = int(round(float(비중[i]) * 27))
        막대 = "█" * 칸 if 칸 > 0 else "▏"
        여백 = " " * (최대폭 - _표시폭(단어들[i]))
        print(f"  {단어들[i]}{여백}  {막대}")


_안내문 = ("※ 이 그림은 이번 계산에서 어느 부분이 상대적으로 더 많이 반영되었는지를 "
           "쉽게 보기 위한 시각화입니다.")


def 확인(문장):
    """메시지 하나를 교육용 모델에 넣고, 어디를 더 많이 참고했는지 보여 줍니다."""
    예측, 단어들, 비중 = _결과(문장)

    print("메시지")
    print("  " + 문장)
    print()
    print(f"AI의 답 : {예측}")
    print()
    _글자막대(단어들, 비중)

    그림, 축 = plt.subplots(figsize=(11.5, 4.4))
    _막대그리기(축, 단어들, 비중, "이번 계산에서 더 많이 참고한 부분")
    그림.subplots_adjust(left=0.04, right=0.98, top=0.84, bottom=0.34)
    그림.text(0.5, 0.03, _안내문, ha="center", fontsize=9.5, color=_보조색)
    plt.show()
    return None


def 비교(문장A, 문장B):
    """두 메시지를 나란히 실행해, 더 많이 참고한 곳이 어떻게 달라지는지 보여 줍니다."""
    예측A, 단어A, 비중A = _결과(문장A)
    예측B, 단어B, 비중B = _결과(문장B)

    for 이름, 문장, 예측 in (("문맥 A", 문장A, 예측A), ("문맥 B", 문장B, 예측B)):
        print(f"[{이름}] {문장}")
        print(f"        AI의 답 : {예측}")
    print()

    그림, 축들 = plt.subplots(1, 2, figsize=(14, 4.6))
    _막대그리기(축들[0], 단어A, 비중A, f"문맥 A  ·  AI의 답 : {예측A}")
    _막대그리기(축들[1], 단어B, 비중B, f"문맥 B  ·  AI의 답 : {예측B}")
    그림.suptitle("같은 요청, 서로 다른 문맥", fontsize=15.5, color=_글자색, y=0.99)
    그림.subplots_adjust(left=0.04, right=0.98, top=0.76, bottom=0.30, wspace=0.14)
    그림.text(0.5, 0.03, _안내문, ha="center", fontsize=9.5, color=_보조색)
    plt.show()
    return None


__all__ = ["준비", "확인", "비교", "긴메시지", "문맥A", "문맥B"]
