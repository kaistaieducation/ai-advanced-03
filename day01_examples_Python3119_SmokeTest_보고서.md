# Day01 Examples Python 3.11.9 Smoke Test 보고서

- **테스트 일자**: 2026-08-10
- **프로젝트 루트**: `C:\work\ai-advanced-03`
- **테스트 대상**: `C:\work\ai-advanced-03\day01\examples`
- **테스트 성격**: 검증 전용 (예제 코드 · requirements 무수정)

---

## 1. 결론

**Day01 examples 3개 파일 전부 Python 3.11.9 / Windows / CPU-only 환경에서 오류 없이 전 셀 실행 완료. FAIL 0건.**

| 항목 | 결과 |
| --- | --- |
| 전체 실행 대상 | 3 (`.ipynb` 3, `.py` 0) |
| PASS | 2 |
| PASS_WITH_WARNING | 1 |
| FAIL | **0** |
| SKIPPED | 0 |
| 성공률 | **100 % (3/3)** |

핵심 사실:

1. 현재 `requirements.txt` 를 **그대로** 설치했을 때 의존성 충돌·wheel 실패·Python 버전 비호환이 **한 건도 없었다.**
2. 3개 노트북의 **모든 코드 셀(35개)이 실행되었고, error 출력은 0건**이다. 학습도 실제로 수렴했다 (CNN 테스트 정확도 98.06 %).
3. 다만 `>=` 만 사용하는 현재 requirements 는 오늘 기준으로 **TensorFlow 2.21.0 / NumPy 2.4.6 / pandas 3.0.5** 라는 매우 최신 조합을 끌어온다. 오늘은 정상 동작하지만, 교육 시점이 달라지면 **교육생마다 다른 버전이 설치되어 재현성이 보장되지 않는다.** 이것이 이번 검증에서 발견된 가장 실질적인 배포 리스크다.
4. 예제 코드 자체를 고쳐야 실행되는 문제는 **없다.** 발견된 2건(kernelspec, 셀 id)은 실행을 막지 않는 메타데이터 위생 문제다.

**최종 판정: B — 경미한 수정 후 배포 가능** (상세 근거는 17장)

---

## 2. 테스트 환경

| 항목 | 값 |
| --- | --- |
| OS | Microsoft Windows NT 10.0.26200.0 (Windows 11 Pro) |
| CPU | 11th Gen Intel(R) Core(TM) i5-1135G7 @ 2.40GHz |
| RAM | 31.7 GB |
| GPU | **없음 (CPU-only)** |
| Python | **3.11.9** |
| uv | **0.11.29** |
| 가상환경 | `C:\work\ai-advanced-03\.venv-py311-test` |
| 인터넷 | 사용 가능 (MNIST 신규 다운로드 검증 완료) |

테스트 시 강제한 환경변수:

```powershell
$env:CUDA_VISIBLE_DEVICES="-1"   # GPU 사용 명시적 차단
$env:TF_CPP_MIN_LOG_LEVEL="2"    # TF 정보성 로그 축소
$env:MPLBACKEND="Agg"            # GUI 창으로 인한 정지 방지
$env:PYTHONIOENCODING="utf-8"    # 한글 출력 깨짐 방지
```

CUDA / cuDNN / NVIDIA 드라이버 의존 패키지 / GPU 전용 TensorFlow 구성은 **설치하지 않았다.**

### 기존 시스템 환경 보호 확인

| 보호 대상 | 처리 |
| --- | --- |
| 시스템 Python 3.12.10 (`C:\Users\yujinkwon\AppData\Local\Programs\Python\Python312`) | 변경 없음 |
| uv 관리 Python 3.14.6 / 3.12.13 | 변경 없음 |
| 전역 site-packages | 변경 없음 |
| 프로젝트 `.venv` | **애초에 존재하지 않았음** — 신규 `.venv-py311-test` 만 생성 |
| `day01/examples/*.ipynb` 원본 | **무수정** (파일 크기·수정시각 테스트 전후 동일) |
| `requirements.txt` | **무수정** |

---

## 3. Python 3.11.9 설치 및 확인 결과

### 3.1 사전 조사

```powershell
py -0p
```

```text
 -V:3.12 *                C:\Users\yujinkwon\AppData\Local\Programs\Python\Python312\python.exe
 -V:Astral/CPython3.14.6  C:\Users\yujinkwon\AppData\Roaming\uv\python\cpython-3.14.6-...\python.exe
 -V:Astral/CPython3.12.13 C:\Users\yujinkwon\AppData\Roaming\uv\python\cpython-3.12.13-...\python.exe
 -V:Astral/CPython3.11.9  C:\Users\yujinkwon\AppData\Roaming\uv\python\cpython-3.11.9-windows-x86_64-none\python.exe
```

- `python --version` → `Python 3.12.10` (시스템 기본)
- `py -3.11 --version` → `No suitable Python runtime found`
  → py launcher 는 uv 관리 Python 을 3.11 로 인식하지 않으나, **실제로는 uv 가 관리하는 CPython 3.11.9 가 이미 설치되어 있었다.**

### 3.2 판단 및 조치

**Python 3.11.9 가 이미 존재하므로 신규 설치를 하지 않았다.**
`https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe` 는 **다운로드·실행하지 않았다.**

사용한 인터프리터:

```text
C:\Users\yujinkwon\AppData\Roaming\uv\python\cpython-3.11.9-windows-x86_64-none\python.exe
```

### 3.3 버전 검증

```powershell
& "...\cpython-3.11.9-windows-x86_64-none\python.exe" --version
```

```text
Python 3.11.9      ← 요구 버전과 정확히 일치
```

---

## 4. uv 및 가상환경 구성

### 4.1 uv

이미 설치되어 있어 **재설치하지 않았다.**

```text
uv 0.11.29 (901092ee1 2026-07-15 x86_64-pc-windows-msvc)
경로: C:\Users\yujinkwon\.local\bin\uv.exe
```

### 4.2 가상환경 생성

기존 `.venv` 는 프로젝트에 **존재하지 않았고**, 동일 이름의 테스트 환경도 없었다.

```powershell
cd C:\work\ai-advanced-03
uv venv .venv-py311-test --python "C:\Users\yujinkwon\AppData\Roaming\uv\python\cpython-3.11.9-windows-x86_64-none\python.exe"
```

```text
Using CPython 3.11.9 interpreter at: ...\cpython-3.11.9-windows-x86_64-none\python.exe
Creating virtual environment at: .venv-py311-test
```

> `uv venv .venv-py311-test --python 3.11.9` 대신 실제 `python.exe` 절대경로를 지정했다. 이는 py launcher 가 3.11 을 인식하지 못하는 상황에서 **3.11.9 가 아닌 다른 버전이 선택될 여지를 없애기 위한 것**이다.

### 4.3 생성 결과 검증

```powershell
.\.venv-py311-test\Scripts\python.exe --version
.\.venv-py311-test\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.version)"
```

```text
Python 3.11.9
C:\work\ai-advanced-03\.venv-py311-test\Scripts\python.exe
3.11.9 (main, Aug 14 2024, 04:18:20) [MSC v.1929 64 bit (AMD64)]
```

요구 버전 **3.11.9 정확히 일치 확인.**

---

## 5. requirements 설치 결과

### 5.1 사용한 requirements 파일

프로젝트 루트에 `requirements.txt` 가 **정확히 존재**하여 그대로 사용했다.

```text
C:\work\ai-advanced-03\requirements.txt   (335 bytes)
```

내용 (원문 그대로, 무수정):

```text
# 대전 국세청 AI 심화 과정 day01~day04 실습 공통 환경
# Python 3.11 (권장 3.11.9) / Windows / CPU-only
#   uv venv --python 3.11
#   uv pip install -r requirements.txt

# day01 / day02 — 딥러닝 · CNN · RNN/LSTM · Attention · Transformer
tensorflow>=2.16
keras>=3.0
numpy>=1.26
pandas
matplotlib
scikit-learn
```

검증 기준으로 제시된 패키지 구성과 **완전히 일치**한다.

> 참고: 루트에 `requirements.txt.bak` (552 bytes) 도 존재한다. 여기에는 `ipykernel` 및 day03 RAG 용 패키지(`langchain-core`, `faiss-cpu`, `psutil` 등)가 추가로 들어 있다. 이번 Day01 검증 범위가 아니므로 **사용하지 않았다.** (13.2절에서 별도 언급)

### 5.2 설치 명령 및 결과

```powershell
uv pip install --python .\.venv-py311-test\Scripts\python.exe -r requirements.txt
```

```text
Using Python 3.11.9 environment at: .venv-py311-test
Resolved 47 packages in 522ms
Installed 47 packages in 28.19s
```

### 5.3 설치 이슈 분석

| 항목 | 결과 |
| --- | --- |
| ERROR | **0건** |
| WARNING | **0건** |
| dependency conflict | **0건** |
| incompatible Python version | **0건** |
| wheel 설치 실패 | **0건** (전 패키지 사전 빌드 wheel, 소스 빌드 없음) |
| 총 소요 시간 | 약 29초 |

`uv` 출력에 나타난 `Using Python 3.11.9 environment at: .venv-py311-test` 는 정보성 메시지다.
(PowerShell 이 native 명령의 stderr 를 `NativeCommandError` 로 감싸 표시하는 것은 PowerShell 표시 방식일 뿐 설치 실패가 아니다.)

**설치 단계에서 실제 오류는 한 건도 없었다.**

### 5.4 테스트 수행용 보조 패키지

`day01/examples` 가 전부 `.ipynb` 이므로 전 셀 실제 실행을 위해 **테스트 도구만** 추가 설치했다.

```powershell
uv pip install --python .\.venv-py311-test\Scripts\python.exe jupyter nbconvert ipykernel
```

이 패키지들은 **교육 예제 필수 패키지가 아니며, `requirements.txt` 를 수정하지 않았다.**
(구분은 6장 참조)

### 5.5 설치 상태 검증 (import 및 CPU 연산)

```text
Python: 3.11.9 (main, Aug 14 2024, 04:18:20) [MSC v.1929 64 bit (AMD64)]
Executable: C:\work\ai-advanced-03\.venv-py311-test\Scripts\python.exe
TensorFlow: 2.21.0
Keras: 3.15.1
NumPy: 2.4.6
Pandas: 3.0.5
Matplotlib: 3.11.1
scikit-learn: 1.9.0
Matplotlib backend: Agg

Physical devices: [PhysicalDevice(name='/physical_device:CPU:0', device_type='CPU')]
GPU devices: []                      ← CPU-only 이므로 정상

matmul: [[19.0, 22.0], [43.0, 50.0]]                 ← CPU 기본 연산 정상
keras fit ok, loss: [0.2164, 0.2128]                 ← CPU 학습 정상
ENV_CHECK_OK
```

전 패키지 import 성공, TensorFlow CPU 연산 및 Keras 학습 모두 정상 동작.

---

## 6. 실제 설치 패키지 버전

### 6.1 핵심 도구

| 항목 | 실제 버전 |
| --- | --- |
| Python | **3.11.9** |
| uv | **0.11.29** |

### 6.2 교육 예제 필수 패키지 (requirements.txt 기준)

| requirements 명세 | 실제 설치 버전 | 비고 |
| --- | --- | --- |
| `tensorflow>=2.16` | **2.21.0** | 명세보다 5 마이너 버전 위 |
| `keras>=3.0` | **3.15.1** | TF 2.21 이 요구하는 버전 |
| `numpy>=1.26` | **2.4.6** | **NumPy 2.x 계열** |
| `pandas` (범위 없음) | **3.0.5** | **pandas 3.x 메이저** |
| `matplotlib` (범위 없음) | **3.11.1** | |
| `scikit-learn` (범위 없음) | **1.9.0** | |

주요 전이 의존성: `scipy 1.17.1`, `h5py 3.14.0`, `protobuf 7.35.1`, `grpcio 1.83.0`, `ml-dtypes 0.5.4`, `optree 0.19.1`, `pillow 12.3.0`, `absl-py 2.5.0`

### 6.3 테스트 수행용 보조 패키지 (requirements.txt 에 없음)

| 패키지 | 실제 버전 |
| --- | --- |
| jupyter | 1.1.1 |
| nbconvert | 7.17.1 |
| ipykernel | 7.3.0 |
| nbclient | 0.11.0 |
| nbformat | 5.11.0 |
| notebook | 7.6.1 |
| jupyterlab | 4.6.2 |
| ipython | 9.16.1 |
| matplotlib-inline | 0.2.2 |

전체 목록은 `day01_examples_Python3119_installed_versions.txt` 참조.

---

## 7. day01/examples 파일 구성

### 7.1 재귀 전수 조사 결과

`C:\work\ai-advanced-03\day01\examples` 를 재귀 조사한 결과 **하위 디렉터리는 없으며, 파일 3개가 전부**다.

| 분류 | 개수 | 파일 |
| --- | --: | --- |
| `.ipynb` (실행 대상) | **3** | `02.deep_learning.ipynb`, `03.cnn.ipynb`, `04.rnn_lstm.ipynb` |
| `.py` (실행 대상) | **0** | — |
| CSV | 0 | — |
| JSON | 0 | — |
| TXT | 0 | — |
| 이미지 | 0 | — |
| 모델 파일 (`.h5`/`.keras`/`.pb`) | 0 | — |
| 기타 데이터 파일 | 0 | — |

| 파일 | 크기 | 코드 셀 | 전체 셀 |
| --- | --: | --: | --: |
| `02.deep_learning.ipynb` | 176,962 B | 9 | 40 |
| `03.cnn.ipynb` | 473,113 B | 13 | 42 |
| `04.rnn_lstm.ipynb` | 142,647 B | 13 | 44 |
| **합계** | | **35** | **126** |

> `day01\lecture-materials` 에 `.pptx` 5개가 있으나 실행 대상이 아니다.
> Day01 examples 에 `01.` 로 시작하는 노트북은 없다 (강의자료 `01.course_overview.pptx` 는 개요 슬라이드로 실습 예제가 아님).

### 7.2 실행 전 정적 검토 (의존성 사전 확인)

| 점검 항목 | 02.deep_learning | 03.cnn | 04.rnn_lstm |
| --- | --- | --- | --- |
| 로컬 파일 의존 | 없음 | 없음 | 없음 |
| CSV / 이미지 / 모델 파일 의존 | 없음 | 없음 | 없음 |
| **인터넷 다운로드** | 없음 | **있음 (MNIST)** | 없음 |
| Keras dataset 자동 다운로드 | 없음 | `tf.keras.datasets.mnist.load_data()` | 없음 |
| 사용자 입력 (`input()`) | 없음 | 없음 | 없음 |
| GUI | 없음 | 없음 | 없음 |
| `matplotlib plt.show()` | 없음 | **있음 (6회)** | 없음 |
| 절대 경로 | 없음 | 없음 | 없음 |
| GPU 명시 요구 | 없음 | 없음 | 없음 |
| API key / 외부 서버 | 없음 | 없음 | 없음 |
| Windows 미지원 기능 | 없음 | 없음 | 없음 |
| 한글 폰트 요구 | 없음 | **있음 (Malgun Gothic 등)** | 없음 |
| 데이터 출처 | 노트북 내장 (민원 문장 54건) | MNIST (외부) | 노트북 내장 (업무 문장 28건) |

**정적 검토 결론**: 외부 의존은 `03.cnn.ipynb` 의 MNIST 다운로드 1건뿐이며, 나머지는 전부 자기완결적(self-contained)이다. 이는 교육 환경으로서 매우 바람직한 구성이다. 이 단계에서 예제 파일은 **수정하지 않았다.**

---

## 8. 전체 Smoke Test 결과

### 8.1 결과 표

| No | 파일 | 형식 | 결과 | 실행 시간 | Warning | Error | 원인 요약 |
| -: | --- | --- | --- | --: | --- | --- | --- |
| 1 | `day01/examples/02.deep_learning.ipynb` | IPYNB | **PASS** | 73.9 s | 없음 (노트북 기인) | 없음 | 정상. 9/9 셀 실행, MLP 학습 수렴 |
| 2 | `day01/examples/03.cnn.ipynb` | IPYNB | **PASS** | 85.2 s | 테스트 하네스 기인만 (Agg) | 없음 | 정상. 13/13 셀 실행, 테스트 정확도 98.06 % |
| 3 | `day01/examples/04.rnn_lstm.ipynb` | IPYNB | **PASS_WITH_WARNING** | 246.2 s | `MissingIDFieldWarning` | 없음 | 실행 정상. 노트북 파일에 셀 `id` 누락 |

`.py` 파일은 0개이므로 해당 표는 없다 (9장 참조).

### 8.2 집계

```text
전체 실행 대상 : 3
PASS               : 2
PASS_WITH_WARNING  : 1
FAIL               : 0
SKIPPED            : 0
성공률             : 100 % (3/3)
```

**FAIL 파일 없음. SKIPPED 파일 없음.**

### 8.3 전 노트북 공통 사항 — kernelspec 불일치 (중요)

세 노트북 모두 존재하지 않는 커널을 지정하고 있다.

| 파일 | 선언된 kernelspec name | display_name |
| --- | --- | --- |
| `02.deep_learning.ipynb` | `kaist-day01` | Python 3.11 (KAIST day01 예제) |
| `03.cnn.ipynb` | `kaist-day01` | Python 3.11 (KAIST day01 예제) |
| `04.rnn_lstm.ipynb` | `kaist-day01` | Python 3.11 (KAIST day01 실습) |

옵션 없이 실행하면 즉시 실패한다:

```text
jupyter_client.kernelspec.NoSuchKernel: No such kernel named kaist-day01
```

- **VS Code 에서는 무해하다.** 학생이 우측 상단에서 인터프리터를 직접 선택하므로 노트북의 kernelspec 은 무시된다. (교육 환경이 VS Code 이므로 실행 차단 요인은 아님)
- **`jupyter nbconvert` / `jupyter lab` / `jupyter notebook` CLI 에서는 하드 에러**다.

따라서 본 Smoke Test 는 커널을 테스트 가상환경으로 명시 지정하여 실행했다:

```powershell
--ExecutePreprocessor.kernel_name=python3
```

이는 **테스트 하네스 설정이며 노트북 원본은 수정하지 않았다.** 권고 조치는 16장 참조.

### 8.4 실행 명령 (실제 사용)

```powershell
cd C:\work\ai-advanced-03\day01\examples          # 예제 위치를 working directory 로 사용

$env:CUDA_VISIBLE_DEVICES="-1"
$env:TF_CPP_MIN_LOG_LEVEL="2"
$env:MPLBACKEND="Agg"
$env:PYTHONIOENCODING="utf-8"

C:\work\ai-advanced-03\.venv-py311-test\Scripts\python.exe -m jupyter nbconvert `
  --to notebook --execute "<원본.ipynb>" `
  --output-dir "C:\work\ai-advanced-03\.test_artifacts" `
  --output "executed_<이름>.ipynb" `
  --ExecutePreprocessor.kernel_name=python3 `
  --ExecutePreprocessor.timeout=1800
```

- 시스템 `python` 명령에 의존하지 않고 테스트 가상환경 `python.exe` 절대경로를 사용했다.
- 실행 결과물은 전부 `.test_artifacts` 에 저장했고 **원본 노트북에 덮어쓰지 않았다.**

### 8.5 "오래 걸렸으니 성공" 이 아님 — 실질 검증

단순 exit code 0 이 아니라 산출물 노트북을 파싱하여 다음을 확인했다.

| 검증 항목 | 02 | 03 | 04 |
| --- | --- | --- | --- |
| 코드 셀 수 | 9 | 13 | 13 |
| `execution_count` 부여된 셀 | **9/9** | **13/13** | **13/13** |
| `output_type == "error"` 출력 | **0** | **0** | **0** |
| 출력이 없는 셀 | 0 | 1 (셀 11) | 3 (셀 6, 8, 11) |
| 학습 수렴 확인 | loss 1.0924 → 0.0030 | acc 0.8550 → 0.9781 | RNN loss 4.308 → 0.057 |

출력이 없는 셀은 전부 **모델 정의 / 함수 정의 셀로 `print` 가 없는 것이 정상**이다 (03 셀 11 = `scores`/`best` 계산, 04 셀 6·11 = `Sequential` 정의, 셀 8 = 헬퍼 함수 정의).

---

## 9. Python 파일별 실행 결과

**`day01/examples` 에 `.py` 파일은 존재하지 않는다 (0개).**

재귀 조사 결과 실행 대상 Python 스크립트가 없으므로 해당 항목은 없다. Day01 실습은 전부 Jupyter Notebook 으로 구성되어 있다.

---

## 10. Notebook 파일별 실행 결과

### 10.1 `02.deep_learning.ipynb` — PASS

| 항목 | 값 |
| --- | --- |
| 상대 경로 | `day01/examples/02.deep_learning.ipynb` |
| 형식 | IPYNB (전체 40셀 / 코드 9셀) |
| 실행 환경 | `.venv-py311-test\Scripts\python.exe` (Python 3.11.9) |
| working directory | `C:\work\ai-advanced-03\day01\examples` |
| 시작 여부 | 정상 시작 |
| 정상 종료 여부 | 정상 종료 |
| exit code | **0** |
| 실행 시간 | **73.9 초** |
| 실행 셀 | 9 / 9 |
| ERROR | **없음** |
| WARNING | **없음** (노트북 기인 warning 0건) |
| 외부 다운로드 | **없음** (데이터 노트북 내장) |
| 결과 | **PASS** |

**주요 stdout**

```text
TensorFlow 버전 : 2.21.0
전체 민원 문장 : 54 건
준비 완료 : 이제 민원 문장을 토큰 ID 로 바꿀 수 있습니다.
MLP 모델이 만들어졌습니다.

[학습 전] 소득금액증명서를 출력하고 싶습니다.
          [0.33  0.334 0.336]   ← 세 점수가 서로 비슷합니다

Epoch 1/20   6/6 - 4s - 643ms/step - loss: 1.0924 - val_loss: 1.0456
Epoch 10/20  6/6 - 0s -  54ms/step - loss: 0.0700 - val_loss: 0.3848
Epoch 20/20  6/6 - 0s -  45ms/step - loss: 0.0030 - val_loss: 0.3613
학습이 끝났습니다.

[학습 후] 학습 전 : [0.33  0.334 0.336]
          학습 후 : [0.999 0.001 0.   ]
          모델이 제안하는 카테고리 : 증명서 발급

사업자등록증명원이 급하게 필요합니다.            → 증명서 발급 [0.996 0.003 0.001]
종합소득세를 인터넷으로 신고하려면 어떻게 하나요?  → 신고·납부   [0.224 0.772 0.004]
홈택스에 접속하려는데 로그인이 계속 실패합니다.    → 홈택스 이용 [0.    0.003 0.997]
```

**stderr**: 없음 (노트북 셀 출력 기준)

**평가**: 학습이 실제로 수렴했고(loss 1.0924 → 0.0030), 세 카테고리 추론 결과가 모두 의도한 정답과 일치한다. 교안의 "학습 전 vs 학습 후" 대비 메시지가 실행 결과로 정확히 재현된다. 한글 변수명(`증명서발급`, `민원_문장` 등)도 Python 3.11.9 에서 문제없이 동작한다.

---

### 10.2 `03.cnn.ipynb` — PASS

| 항목 | 값 |
| --- | --- |
| 상대 경로 | `day01/examples/03.cnn.ipynb` |
| 형식 | IPYNB (전체 42셀 / 코드 13셀) |
| 실행 환경 | `.venv-py311-test\Scripts\python.exe` (Python 3.11.9) |
| working directory | `C:\work\ai-advanced-03\day01\examples` |
| 시작 여부 | 정상 시작 |
| 정상 종료 여부 | 정상 종료 |
| exit code | **0** |
| 실행 시간 | **85.2 초** (Agg) / **84.0 초** (inline 재실행) |
| 실행 셀 | 13 / 13 |
| ERROR | **없음** |
| WARNING | `FigureCanvasAgg is non-interactive` × 6 → **테스트 하네스 기인, 노트북 결함 아님** |
| 외부 다운로드 | **있음 — MNIST (약 11 MB)** |
| 결과 | **PASS** |

**주요 stdout**

```text
TensorFlow 버전 : 2.21.0
준비 완료

학습용 이미지 : (60000, 28, 28)   → 60,000장
테스트 이미지 : (10000, 28, 28)   → 10,000장
밝기값 범위   : 0 ~ 255
학습 이미지 : (60000, 28, 28, 1)  밝기값 범위 : 0.0 ~ 1.0

Epoch 1/5  422/422 - 9s - 20ms/step - accuracy: 0.8550 - loss: 0.5204 - val_accuracy: 0.9642
Epoch 5/5  422/422 - 8s - 19ms/step - accuracy: 0.9781 - loss: 0.0706 - val_accuracy: 0.9817

Loss     : 0.5204  →  0.0706
Accuracy : 0.8550  →  0.9781

conv1 출력         : (26, 26, 8) → 26 × 26 Feature Map 8장
Feature Map 값 범위 : 0.000 ~ 2.059 (ReLU를 지나 음수는 모두 0)
칸 수          : 676 → 169
가장 강한 반응 : 1.296 → 1.296

  8 : 0.9989  ← 가장 높은 후보
  합계 : 1.0000
→ 가장 높은 8 를 예측 후보로 선택합니다.

Test Accuracy : 0.9806   (10,000장 중 9,806장 정답)
틀린 이미지   : 194장
```

**MNIST 다운로드 검증**

테스트 PC 에는 `C:\Users\yujinkwon\.keras\datasets\mnist.npz` 가 이미 캐시되어 있었다. **캐시 덕분에 통과한 것으로 오판하지 않기 위해**, `KERAS_HOME` 을 빈 디렉터리로 지정하여 신규 다운로드 경로를 별도로 검증했다.

```text
FRESH_DOWNLOAD_OK (60000, 28, 28) (10000, 28, 28) 21.2 s
```

→ **캐시가 전혀 없는 교육생 PC 에서도 MNIST 다운로드가 정상 동작한다** (약 11 MB, TF import 포함 21.2초).

**matplotlib / 그래프 검증**

`MPLBACKEND="Agg"` 로 실행하면 `plt.show()` 가 6회 `UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown` 를 낸다. 이는 **GUI 없는 백엔드를 강제한 테스트 하네스 때문이며 노트북 코드 결함이 아니다.**

이를 확정하기 위해 `MPLBACKEND` 를 제거하고 **커널 기본 inline 백엔드(= VS Code 학생 환경과 동일)로 전체 재실행**했다.

| 실행 조건 | exit code | 실행 시간 | 생성된 `image/png` | Agg warning |
| --- | --- | --: | --: | --- |
| `MPLBACKEND=Agg` | 0 | 85.2 s | 0 | 6회 |
| 기본 inline 백엔드 | **0** | 84.0 s | **6** | **0회** |

→ **그래프 6개가 모두 정상 렌더링되었고 warning 은 완전히 사라졌다.** 그래프 생성 코드 자체에 문제가 없음을 확정한다.

**한글 폰트 검증**

노트북은 `Malgun Gothic → NanumGothic → AppleGothic` 순으로 폰트를 탐색한다. 테스트 PC 확인 결과:

```text
Malgun Gothic -> True      ← Windows 기본 탑재. 첫 후보에서 매칭
NanumGothic   -> True
AppleGothic   -> False     (macOS 전용, Windows 에 없는 것이 정상)
```

→ Windows 교육생 PC 는 `Malgun Gothic` 이 기본 탑재되므로 **그래프 한글 라벨이 깨지지 않는다.** `axes.unicode_minus = False` 설정도 되어 있어 음수 기호 깨짐도 방지된다.

**평가**: 5 epoch 학습으로 테스트 정확도 98.06 % 달성. CPU 로 약 8~9초/epoch 이며 전체 85초로, 강의 중 실행하기에 적절한 규모다. Feature Map 시각화·Pooling 전후 비교·오분류 사례까지 전부 정상 동작한다.

---

### 10.3 `04.rnn_lstm.ipynb` — PASS_WITH_WARNING

| 항목 | 값 |
| --- | --- |
| 상대 경로 | `day01/examples/04.rnn_lstm.ipynb` |
| 형식 | IPYNB (전체 44셀 / 코드 13셀) |
| 실행 환경 | `.venv-py311-test\Scripts\python.exe` (Python 3.11.9) |
| working directory | `C:\work\ai-advanced-03\day01\examples` |
| 시작 여부 | 정상 시작 |
| 정상 종료 여부 | 정상 종료 |
| exit code | **0** |
| 실행 시간 | **246.2 초** (약 4분 6초 — 3개 중 가장 김) |
| 실행 셀 | 13 / 13 |
| ERROR | **없음** |
| WARNING | `MissingIDFieldWarning` (노트북 파일 기인), oneDNN `DT_BOOL` 안내 (정보성) |
| 외부 다운로드 | **없음** (데이터 노트북 내장) |
| 결과 | **PASS_WITH_WARNING** |

**주요 stdout**

```text
TensorFlow 버전 : 2.21.0
NumPy 버전      : 2.4.6

문장 수 : 28 개
단어 사전 크기 VOCAB_SIZE : 75 개
입력 칸 개수    MAX_LEN    : 13 칸

"자료를 확인하고 담당자에게"  ↓  [4, 40, 6]  ↓  ['자료를', '확인하고', '담당자에게']

만들어진 학습 문제 수 : 158 개
입력 X 의 모양        : (158, 13)
정답 y 의 모양        : (158,)

RNN Loss: 4.308 → 0.057
→ Loss(손실)가 줄어들었다면 학습이 진행된 것입니다.

입력 : "자료를 확인하고 담당자에게 ___"     1. 전달했습니다  0.996
입력 : "회의 자료를 검토한 후 결과를 ___"    1. 공유했습니다  0.994
입력 : "신청서를 접수한 후 민원인에게 ___"   1. 안내했습니다  0.996

[정상 순서] "자료를 확인하고 담당자에게 ___"  → 1. 전달했습니다 0.996
[순서 변경] "담당자에게 자료를 확인하고 ___"  → 1. 검토한 0.354 / 2. 정리한 0.250

LSTM Loss: 4.316 → 0.083

입력 : "자료를 확인하고 담당자에게 ___"
  SimpleRNN 1순위 : 전달했습니다  (0.996)
  LSTM      1순위 : 전달했습니다  (0.990)
```

**WARNING 상세**

1. **`MissingIDFieldWarning` — 노트북 파일 자체의 결함 (실행 차단 아님)**

   ```text
   nbformat\validator.py:434: MissingIDFieldWarning: Cell is missing an id field,
   this will become a hard error in future nbformat versions.
   ```

   조사 결과:

   | 파일 | nbformat | `id` 누락 셀 |
   | --- | --- | --: |
   | `02.deep_learning.ipynb` | 4.5 | 0 |
   | `03.cnn.ipynb` | 4.5 | 0 |
   | `04.rnn_lstm.ipynb` | 4.5 | **44 (전 셀)** |

   `04.rnn_lstm.ipynb` 는 nbformat **4.5** 를 선언하면서 44개 셀 **전부**에 4.5 규격 필수 필드인 `id` 가 없다. 현재 nbformat 5.11.0 은 경고 후 자동 보정하지만, **향후 버전에서 하드 에러로 바뀐다고 명시**되어 있다. 지금은 실행에 영향이 없다.

2. **oneDNN `DT_BOOL` 안내 — 정보성 (오류 아님)**

   ```text
   E0000 util.cc:131] oneDNN supports DT_BOOL only on platforms with AVX-512.
   Falling back to the default Eigen-based implementation if present.
   ```

   `E0000` 로 표시되어 오류처럼 보이지만 **실제로는 정보성 fallback 안내**다. 테스트 CPU(i5-1135G7)는 AVX-512 미지원이므로 기본 Eigen 구현으로 되돌아갔을 뿐이며, 연산 결과와 학습에는 아무 영향이 없다 (RNN loss 4.308 → 0.057 정상 수렴). `mask_zero=True` 로 인한 bool 마스크 연산에서 발생한다. **오류로 분류하지 않는다.**

**실행 시간 분석**: 246초 중 대부분은 SimpleRNN 300 epoch + LSTM 300 epoch 학습이다. 데이터가 158건으로 매우 작아 epoch 당 시간은 짧지만 총 600 epoch 이라 누적된다. 강의 중 학생 PC 성능에 따라 **4~8분** 소요될 수 있어 사전 안내가 필요하다 (15장 참조).

**평가**: RNN 과 LSTM 모두 정상 학습·수렴했고, 교안의 핵심 메시지("단어 순서가 바뀌면 예측이 달라진다")가 실행 결과로 명확히 재현된다. 긴 문맥 비교까지 정상 동작한다.

---

## 11. Warning 분석

발생한 모든 warning 을 **원인 주체별로** 분류했다.

### 11.1 노트북 파일 기인 (조치 권고)

| Warning | 발생 파일 | 심각도 | 설명 |
| --- | --- | --- | --- |
| `MissingIDFieldWarning` | `04.rnn_lstm.ipynb` | **낮음 (장래 위험)** | nbformat 4.5 선언 대비 44개 전 셀에 `id` 필드 없음. 현재는 자동 보정되나 향후 nbformat 에서 하드 에러 예고 |
| `NoSuchKernel: kaist-day01` | **3개 전부** | **중간** | 미설치 커널 지정. VS Code 는 무해하나 Jupyter CLI/Lab 에서는 실행 불가 |

### 11.2 TensorFlow 정보성 메시지 (정상 — 오류 아님)

| 메시지 | 분류 |
| --- | --- |
| `oneDNN custom operations are on. You may see slightly different numerical results...` | **정상 정보성.** CPU 최적화(oneDNN) 활성 안내 |
| `WARNING: All log messages before absl::InitializeLog() is called are written to STDERR` | **정상 정보성.** absl 로깅 초기화 순서 안내 |
| `WARNING:tensorflow:TensorFlow GPU support is not available on native Windows for TensorFlow >= 2.11...` | **정상 정보성.** TF 2.11+ Windows 네이티브는 GPU 미지원. **CPU-only 교육 환경에서 예상된 정상 메시지** |
| `E0000 util.cc:131] oneDNN supports DT_BOOL only on platforms with AVX-512. Falling back...` | **정상 정보성.** `E` 접두사이나 실제로는 fallback 안내. 결과에 영향 없음 |

> 위 4건은 전부 **GPU 부재 또는 CPU 최적화 관련 안내**이며 실행 오류가 아니다. 다만 교육생이 붉은 글씨를 보고 "에러 났다"고 오해할 소지가 크므로 15장에서 별도 다룬다.

### 11.3 테스트 하네스 기인 (교육생 환경에서는 미발생)

| Warning | 원인 | 교육생 재현성 |
| --- | --- | --- |
| `UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown` × 6 | 본 테스트가 `MPLBACKEND=Agg` 를 강제 | **미발생.** inline 백엔드 재실행 시 0회 확인 |
| `RuntimeWarning: Proactor event loop does not implement add_reader...` (zmq) | `nbconvert` CLI 실행 방식 | **미발생.** VS Code 실행 시 해당 없음 |
| `[IPKernelApp] WARNING | Kernel is running over TCP without encryption` | `nbconvert` 가 띄운 임시 커널 | **미발생** |
| PowerShell `NativeCommandError` | PowerShell 이 native stderr 를 감싸 표시 | 표시 방식일 뿐, 실패 아님 |

### 11.4 발생하지 않은 warning

`DeprecationWarning`, `FutureWarning`, Keras API deprecation warning 은 **한 건도 발생하지 않았다.** TensorFlow 2.21 / Keras 3.15 에서 사용 중단 예정 API 를 쓰지 않았다는 뜻으로, 예제 코드가 Keras 3 스타일로 잘 작성되어 있음을 보여준다.

특히 다음 API 들이 최신 스택에서 정상 동작함을 확인했다.

- `tf.keras.layers.TextVectorization` (`split="character"`, `standardize=None`, `split="whitespace"`)
- `tf.keras.layers.Embedding(mask_zero=True)` + `GlobalAveragePooling1D`
- `tf.keras.Input(shape=(1,), dtype=tf.string)` — 문자열 입력을 Sequential 모델에 직접 투입
- `tf.keras.utils.pad_sequences`
- `tf.keras.Model(inputs=model.inputs, outputs=[...])` — 중간층 추출(Feature Map peek)
- `tf.keras.utils.set_random_seed`

---

## 12. 실패 파일 상세 분석

**FAIL 파일: 없음 (0건)**
**SKIPPED 파일: 없음 (0건)**

3개 파일 전부 전 셀이 실제로 실행되었고 error 출력이 0건이므로, 본 장에서 상세 분석할 대상이 없다.

참고로, 아래 1건은 **파일 실패가 아니라 실행 방식(하네스) 이슈**로서 초기에 재현되었기에 형식에 맞춰 기록한다.

### 참고: kernelspec 미설치로 인한 nbconvert 초기 실행 실패

**경로**: `day01/examples/*.ipynb` (3개 전부 해당)

**실행 환경**: `.venv-py311-test` (Python 3.11.9), Windows 11, CPU-only

**실행 명령**:
```powershell
python -m jupyter nbconvert --to notebook --execute "02.deep_learning.ipynb" --ExecutePreprocessor.timeout=60
```

**결과**: 커널 옵션 미지정 시 실패 → **커널 지정 후 재실행하여 PASS**

**오류 메시지**:
```text
File ".../jupyter_client/kernelspec.py", line 287, in get_kernel_spec
    raise NoSuchKernel(kernel_name)
jupyter_client.kernelspec.NoSuchKernel: No such kernel named kaist-day01
```

**직접 원인**: 노트북 메타데이터의 `metadata.kernelspec.name` 이 `kaist-day01` 인데, 해당 이름의 Jupyter 커널이 시스템에 등록되어 있지 않다.

**근본 원인**: 노트북을 제작한 PC 에서 `python -m ipykernel install --name kaist-day01` 로 커스텀 커널을 등록해 사용했고, 그 메타데이터가 파일에 저장된 채 배포되었다. 커널 등록은 사용자 환경(`%APPDATA%\jupyter\kernels`)에 있으므로 파일과 함께 전달되지 않는다.

**Python 3.11.9 호환성 문제 여부**: **아님.** Python 버전과 무관하다.

**requirements 문제 여부**: **아님.** 패키지 설치 상태와 무관하다.

**예제 코드 문제 여부**: **코드 문제 아님. 노트북 메타데이터 문제.** 어떤 코드 셀도 수정할 필요가 없다.

**권장 수정 방법** (셋 중 택1, 본 테스트에서는 미적용):
1. **(권장)** 노트북 `metadata.kernelspec.name` 을 표준값 `python3` / display_name `Python 3` 로 변경 → 어떤 환경에서도 무난
2. 교육 안내서에 커널 등록 절차 추가:
   `uv pip install ipykernel` 후 `python -m ipykernel install --user --name kaist-day01 --display-name "Python 3.11 (KAIST day01)"`
3. VS Code 사용을 전제로 하고, "우측 상단에서 `.venv` 인터프리터를 선택하세요" 안내로 대체

**교육생 PC 에서 재현 가능성**:
- **VS Code 로 실습하는 경우 → 재현되지 않음** (학생이 커널을 직접 선택하므로 무해). 교육 환경이 VS Code 이므로 실습 차단 요인은 아니다.
- **`jupyter lab` / `jupyter notebook` / `nbconvert` 를 쓰는 경우 → 100 % 재현**되며 노트북이 아예 열리거나 실행되지 않는다.
- VS Code 에서도 커널 선택 드롭다운에 "Python 3.11 (KAIST day01 예제)" 가 회색으로 표시되어 학생이 혼란을 느낄 수 있다.

---

## 13. requirements 적정성 검토

검토 대상 (원본 무수정):

```text
tensorflow>=2.16
keras>=3.0
numpy>=1.26
pandas
matplotlib
scikit-learn
```

### 13.1 항목별 검토

| # | 검토 항목 | 판정 | 근거 |
| --- | --- | --- | --- |
| 1 | 불필요한 패키지가 있는가 | **판단 보류** | Day01 예제는 `pandas`, `scikit-learn` 을 **전혀 import 하지 않는다.** 다만 이 파일은 헤더에 명시된 대로 **day01~day04 공통 환경** 파일이고 현재 리포지터리에는 day01 만 존재하므로, day02~day04 에서의 필요 여부를 확인할 수 없다. **Day01 기준으로만 불필요하며, 제거를 권고하지 않는다.** |
| 2 | 필요한데 누락된 패키지가 있는가 | **있음 — `ipykernel`** | 예제가 전부 `.ipynb` 인데 노트북 실행에 필수인 `ipykernel` 이 없다. VS Code 는 없으면 설치를 안내하지만, 환경 설정 경험이 적은 교육생에게는 걸림돌이다. 실제로 `requirements.txt.bak` 에는 `# .ipynb 실행 (VS Code)` 주석과 함께 `ipykernel` 이 들어 있다 — **현재 `requirements.txt` 에서 누락된 것으로 보인다.** |
| 3 | 버전 범위가 너무 넓은가 | **넓다 (핵심 리스크)** | `tensorflow>=2.16` 은 오늘 **2.21.0** 을 가져온다. `pandas`/`matplotlib`/`scikit-learn` 은 상한도 하한도 없다. 실제로 **pandas 3.0.5** 라는 메이저 버전이 설치되었다. 상한이 없으면 교육 시점마다 조합이 달라진다. |
| 4 | Python 3.11.9 와 실제 호환되는가 | **완전 호환 (단, 여유 없음)** | 47개 패키지 전부 사전 빌드 wheel 로 설치, 소스 빌드 0건, 충돌 0건, 29초 완료. 다만 `numpy`·`pandas`·`scikit-learn`·`matplotlib`·`keras` 의 설치된 버전은 이미 `Requires-Python >=3.11` 이라 3.11.9 가 **최소 지원선**이다 (14.1절). |
| 5 | 최신 설치 결과가 Day01 예제와 호환되는가 | **호환** | TF 2.21.0 / Keras 3.15.1 / NumPy 2.4.6 / pandas 3.0.5 조합에서 3개 노트북 35개 셀 전부 정상. Deprecation/Future warning 0건. |
| 6 | 버전을 고정할 필요가 있는가 | **필요** | 14장·25항 참조. |

### 13.2 `requirements.txt` vs `requirements.txt.bak` 차이

| 패키지 | requirements.txt | requirements.txt.bak |
| --- | --- | --- |
| tensorflow / keras / numpy / pandas / matplotlib / scikit-learn | 있음 | 있음 (동일) |
| **ipykernel** | **없음** | **있음** |
| langchain-core / langchain-text-splitters / langchain-ollama / langchain-community | 없음 | 있음 (day03 RAG) |
| faiss-cpu / psutil | 없음 | 있음 (day03 RAG) |

`.bak` 은 day03 RAG 패키지까지 포함한 더 넓은 버전으로 보인다. 어느 쪽이 최종본인지는 과정 운영 계획에 달려 있으나, **적어도 `ipykernel` 은 Day01 실습에 필요하므로 현재 `requirements.txt` 에서 빠진 것이 의도된 것인지 확인이 필요하다.**

---

## 14. Python 3.11.9 / CPU-only 호환성

### 14.1 Python 3.11.9 호환성

| 검증 항목 | 결과 |
| --- | --- |
| 47개 패키지 wheel 설치 | **전부 성공** (소스 빌드 0건) |
| Python 3.11 미지원으로 인한 설치 거부 | **0건** |
| 한글 변수명·함수명 (`민원_문장`, `다음단어_데이터_만들기` 등) | **정상 동작** |
| UTF-8 한글 출력 | **정상** (`PYTHONIOENCODING=utf-8` 사용) |
| 3개 노트북 35개 셀 | **전부 정상 실행** |

**Python 3.11.9 기인 문제: 0건.**

**설치된 패키지의 `Requires-Python` 선언 (실측)**

| 패키지 | 버전 | Requires-Python |
| --- | --- | --- |
| tensorflow | 2.21.0 | `>=3.10` |
| keras | 3.15.1 | `>=3.11` |
| numpy | 2.4.6 | `>=3.11` |
| pandas | 3.0.5 | `>=3.11` |
| scikit-learn | 1.9.0 | `>=3.11` |
| matplotlib | 3.11.1 | `>=3.11` |

6개 중 5개가 **Python 3.11 이상**을 요구한다. 즉 현재 `>=` 범위가 끌어오는 최신 조합은 이미 **Python 3.10 이하를 지원하지 않는다.** 상한이 없으므로 앞으로도 최소 요구 버전이 계속 올라가며, 언젠가 `>=3.12` 를 요구하는 릴리스가 나오면 **Python 3.11.9 고정 환경에서 설치가 깨진다.** 13.1절 항목 3(버전 범위가 너무 넓음)과 16.1절 버전 고정 권고의 추가 근거다.

현 시점에서는 Python 3.11.9 가 6개 패키지 전부의 요구 조건을 충족하므로 문제가 없다.

### 14.2 CPU-only 호환성

| 검증 항목 | 결과 |
| --- | --- |
| `tf.config.list_physical_devices()` | `[PhysicalDevice(name='/physical_device:CPU:0', device_type='CPU')]` |
| `tf.config.list_physical_devices("GPU")` | `[]` — **CPU-only 이므로 정상** |
| CUDA / cuDNN 설치 | **하지 않음** |
| GPU 부재로 인한 실행 실패 | **0건** |
| CPU 기본 연산 (`tf.matmul`) | 정상 |
| CPU 학습 (MLP / CNN / SimpleRNN / LSTM) | **전부 정상 수렴** |

**GPU 미탑재로 인해 실패한 예제는 없다.** 예제 어디에도 GPU 를 명시적으로 요구하는 코드가 없고, 모델 규모가 작아 CPU 로 충분하다.

**CPU 실행 시간 (i5-1135G7 기준)**

| 노트북 | 학습 규모 | 실행 시간 |
| --- | --- | --: |
| 02.deep_learning | MLP, 54문장 × 20 epoch | 73.9 s |
| 03.cnn | CNN(8/16 filters), MNIST 60,000장 × 5 epoch | 85.2 s |
| 04.rnn_lstm | SimpleRNN 300 epoch + LSTM 300 epoch, 158문제 | 246.2 s |
| **합계** | | **약 6분 45초** |

세 노트북 모두 GPU 없이 강의 중 실행 가능한 수준이다.

> **주의**: 위 시간은 i5-1135G7 / RAM 32 GB 기준이다. 교육생 PC 사양이 낮으면 **1.5~2배** 소요될 수 있으며, 특히 `04.rnn_lstm.ipynb` 는 **8분 이상** 걸릴 가능성이 있다.

---

## 15. 교육생 PC 배포 시 예상 문제

교육 환경 전제: Windows PC / Python 3.11.9 / GPU 없음 / uv 사용 / 교육생은 AI·Python 환경 설정 경험이 많지 않을 수 있음.

| # | 예상 문제 | 발생 가능성 | 영향 | 대응 |
| --- | --- | --- | --- | --- |
| 1 | **`>=` 범위로 인한 버전 불일치** — 교육일에 따라 서로 다른 TF/NumPy/pandas 설치 | **높음** | 강사 화면과 학생 화면의 출력·경고가 달라짐. 최악의 경우 미래 버전에서 breaking change 발생 | 버전 고정 (16장) |
| 2 | **`ipykernel` 누락** — 노트북 실행에 필수인데 requirements 에 없음 | **높음** | VS Code 가 설치를 안내하지만 초보자는 당황 | requirements 에 `ipykernel` 추가 |
| 3 | **kernelspec `kaist-day01`** — 커널 드롭다운에 없는 커널이 표시됨 | **높음** | VS Code 는 인터프리터 선택으로 해결되나 혼란 유발. Jupyter CLI 사용 시 완전 차단 | kernelspec 을 `python3` 로 정규화 |
| 4 | **TF 정보성 메시지를 오류로 오해** — `oneDNN...`, `E0000 ... DT_BOOL`, `GPU support is not available` 등이 붉게 표시 | **매우 높음** | "에러가 났다"는 문의 폭주 | 교재에 "정상 메시지" 예시 캡처와 설명 수록 |
| 5 | **`04.rnn_lstm.ipynb` 실행 시간** — 600 epoch 학습으로 저사양 PC 에서 8분+ | **중간** | 학생이 멈춘 줄 알고 커널 중단 | `verbose=0` 이라 진행 표시가 없으므로 "4~8분 걸립니다" 사전 안내 필수 |
| 6 | **MNIST 최초 다운로드 (약 11 MB)** — `03.cnn.ipynb` | **중간** | 기관 방화벽/프록시 환경에서 `storage.googleapis.com` 차단 시 실패 | 사전에 `mnist.npz` 를 배포하거나 네트워크 허용 확인. 본 테스트에서는 신규 다운로드 21.2초로 정상 |
| 7 | **TensorFlow 최초 import 지연** — 8~18초 소요 | **중간** | 학생이 멈춘 줄 알고 재실행 | "첫 셀은 10~20초 걸립니다" 안내 |
| 8 | **설치 용량** — TF 스택 + jupyter 포함 시 수 GB | 낮음 | 저용량 노트북에서 디스크 부족 | 사전 공지 |
| 9 | 한글 폰트 미탑재로 그래프 라벨 깨짐 | **낮음** | 그래프 가독성 | Windows 는 `Malgun Gothic` 기본 탑재 확인 완료. **실질적 위험 없음** |
| 10 | 한글 경로/사용자명으로 인한 문제 | 낮음 | — | 본 테스트 경로는 영문. 예제가 파일 I/O 를 하지 않아 위험 낮음 |

---

## 16. 수정 권고사항

> 아래는 **권고안이며 본 검증 단계에서 실제로 적용하지 않았다.** 예제 코드·requirements 원본은 모두 무수정 상태다.

### 16.1 우선순위 1 — 재현성 확보 (버전 고정)

현재 `>=` 만 사용하는 requirements 는 오늘 정상이지만 교육 시점이 달라지면 조합이 달라진다. 본 테스트에서 **실제로 검증된 조합**으로 고정할 것을 권고한다.

```text
# 검증 완료 조합 (2026-08-10 / Python 3.11.9 / Windows / CPU-only)
tensorflow==2.21.0
keras==3.15.1
numpy==2.4.6
pandas==3.0.5
matplotlib==3.11.1
scikit-learn==1.9.0
ipykernel==7.3.0
```

완전 고정이 부담스러우면 최소한 상한을 두는 절충안:

```text
tensorflow>=2.16,<2.22
keras>=3.0,<3.16
numpy>=1.26,<2.5
pandas<3.1
matplotlib<3.12
scikit-learn<2.0
ipykernel
```

### 16.2 우선순위 2 — `ipykernel` 추가

Day01 예제가 전부 `.ipynb` 이므로 `ipykernel` 은 **선택이 아니라 필수**다. `requirements.txt.bak` 에는 이미 들어 있으므로 현재 파일에서 빠진 것이 의도치 않은 누락일 가능성이 있다.

### 16.3 우선순위 3 — kernelspec 정규화 (3개 파일 전부)

각 노트북의 `metadata.kernelspec` 을 표준값으로 변경:

```json
"kernelspec": {
  "display_name": "Python 3",
  "language": "python",
  "name": "python3"
}
```

→ VS Code·JupyterLab·nbconvert 어디서든 동작한다. **코드 셀은 전혀 건드리지 않는다.**

### 16.4 우선순위 4 — `04.rnn_lstm.ipynb` 셀 `id` 부여

44개 전 셀에 nbformat 4.5 필수 필드인 `id` 가 없다. 아래로 일괄 정규화 가능하다.

```python
import nbformat
nb = nbformat.read("04.rnn_lstm.ipynb", as_version=4)
nbformat.validate(nb)          # normalize 수행
nbformat.write(nb, "04.rnn_lstm.ipynb")
```

또는 VS Code / JupyterLab 에서 한 번 열어 저장하면 자동 부여된다. 지금은 실행에 지장이 없으나, 향후 nbconvert 오류를 예방한다.

### 16.5 우선순위 5 — 교재/안내서 보완 (코드 수정 불필요)

1. **"이 메시지는 정상입니다" 페이지 추가** — 아래 4종 캡처와 설명

   ```text
   oneDNN custom operations are on. You may see slightly different numerical results...
   WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
   WARNING:tensorflow:TensorFlow GPU support is not available on native Windows for TensorFlow >= 2.11...
   E0000 ... oneDNN supports DT_BOOL only on platforms with AVX-512. Falling back to ...
   ```

2. **실행 시간 안내** — 첫 셀(TF import) 10~20초, `03.cnn` 약 1.5분, `04.rnn_lstm` **4~8분** (진행 표시 없음)

3. **환경 구축 절차 명문화**

   ```powershell
   cd C:\work\ai-advanced-03
   uv venv .venv --python 3.11.9
   .\.venv\Scripts\activate
   uv pip install -r requirements.txt
   # VS Code 에서 노트북 열기 → 우측 상단 커널 선택 → .venv 선택
   ```

4. **오프라인/방화벽 대비** — `03.cnn.ipynb` 용 `mnist.npz` 를 `%USERPROFILE%\.keras\datasets\` 에 사전 배포하는 절차 준비

---

## 17. 최종 판정

### 판정: **B — 경미한 수정 후 배포 가능**

### 판정 근거

**A(현재 그대로 배포 가능)가 아닌 이유**

기술적으로는 A 도 성립한다. 오늘 기준으로 `requirements.txt` 를 그대로 설치하면 Day01 예제 3개가 100 % 정상 실행되며, **예제 코드를 한 줄도 고칠 필요가 없다.** 그러나 다음 두 가지 때문에 A 로 판정하지 않는다.

1. **재현성 미확보 (핵심)** — `tensorflow>=2.16` 은 오늘 2.21.0 을, `pandas` 는 무제한이라 3.0.5(메이저)를 가져왔다. 상한이 전혀 없어 교육 실시 시점에 따라 교육생마다 다른 조합이 설치된다. 강사와 학생의 화면이 달라지고, 향후 breaking change 를 그대로 흡수하게 된다. **교육용 배포물로서는 반드시 보완해야 할 지점**이다.
2. **`ipykernel` 누락** — Day01 예제가 전부 `.ipynb` 인데 노트북 실행 필수 패키지가 requirements 에 없다. `requirements.txt.bak` 에는 있으므로 누락 가능성이 높다.

**C(requirements 수정 필요)·D(예제 코드 수정 필요)·E 가 아닌 이유**

- **C 아님**: requirements 로 인한 **설치 실패·의존성 충돌·실행 실패가 0건**이다. 47개 패키지가 wheel 로 29초에 설치되었다. 권고하는 것은 "동작하게 만들기 위한 수정"이 아니라 "재현성을 위한 고정"이다.
- **D 아님**: **예제 코드 셀은 수정할 필요가 전혀 없다.** 35개 코드 셀 전부 정상 실행, error 0건, deprecation warning 0건. 권고 사항 2건(kernelspec, 셀 id)은 **메타데이터**이지 코드가 아니다.
- **E 아님**: 위 두 가지 모두 해당하지 않는다.

### 판정 요약

| 구분 | 상태 |
| --- | --- |
| Python 3.11.9 호환성 | **문제 없음** |
| Windows 호환성 | **문제 없음** |
| CPU-only 실행 | **문제 없음** |
| requirements 설치 | **문제 없음** (오류·충돌 0건) |
| 예제 코드 실행 | **문제 없음** (3/3 PASS, error 0건) |
| 예제 코드 수정 필요성 | **없음** |
| 보완 필요 사항 | 버전 고정 · `ipykernel` 추가 · kernelspec 정규화 · 셀 id 부여 |

**Day01 실습 예제는 Python 3.11.9 / Windows / CPU-only 환경에서 그대로 실행 가능하다. 16.1~16.4 의 경미한 보완(코드 무관, 메타데이터·버전 명세 수준)을 적용하면 교육 배포 준비가 완료된다.**

---

## 부록 A. 산출물 파일

| 파일 | 내용 |
| --- | --- |
| `day01_examples_Python3119_SmokeTest_보고서.md` | 본 보고서 |
| `day01_examples_Python3119_installed_versions.txt` | 실제 설치 버전 전체 기록 |
| `.test_artifacts/executed_02.deep_learning.ipynb` | 02 실행 결과본 (원본 무수정) |
| `.test_artifacts/executed_03.cnn.ipynb` | 03 실행 결과본 (Agg) |
| `.test_artifacts/executed_inline_03.cnn.ipynb` | 03 실행 결과본 (inline, 그래프 6개 포함) |
| `.test_artifacts/executed_04.rnn_lstm.ipynb` | 04 실행 결과본 |
| `.test_artifacts/run_*.log` | 노트북별 실행 로그 |
| `.test_artifacts/install_requirements.log` | requirements 설치 로그 |
| `.test_artifacts/install_testtools.log` | 테스트 도구 설치 로그 |
| `.test_artifacts/env_check.log` | import / CPU 연산 검증 로그 |
| `.test_artifacts/pip_list.txt`, `pip_freeze.txt` | 설치 패키지 목록 |
| `.test_artifacts/nb_summary.tsv` | 노트북별 exit code · 실행 시간 |
| `.test_artifacts/nb_code_dump.txt` | 정적 검토용 코드 셀 덤프 |
| `.test_artifacts/verify_executed.txt` | 실행 결과본 검증 출력 |

## 부록 B. 준수 사항 확인

| 금지 항목 | 준수 여부 |
| --- | --- |
| 예제 코드 임의 수정 | **하지 않음** (파일 크기·수정시각 테스트 전후 동일) |
| Notebook 원본 수정 | **하지 않음** (결과물은 전부 `.test_artifacts` 에 저장) |
| requirements 임의 수정 | **하지 않음** |
| 학습 결과 개선을 위한 코드 변경 | **하지 않음** |
| 오류 은닉용 try/except 추가 | **하지 않음** |
| 에러 파일 삭제 / 실패 파일 테스트 제외 | **하지 않음** (실패 파일 자체가 없음) |
| 시스템 Python 패키지 변경 | **하지 않음** |
| 기존 Python 제거 | **하지 않음** |
| CUDA / GPU 환경 설치 | **하지 않음** |
