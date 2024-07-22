# 🖥️ computer-architecture-projects

## 🗝️ Technology Stack
**Development Environment**: Linux 서버

**Programming Language**: Python


## 🧀 Implementation Challenges
1. 명령어 해석 및 실행
   - 다양한 RISC-V 명령어를 해석하고 실행하는 과정에서 발생하는 문제를 해결하는 데 많은 시간과 노력이 필요했습니다. 특히, 분기 및 점프 명령어의 정확한 구현이 중요한 도전 과제였습니다.
2. 메모리 오류 처리
   - 유효하지 않은 메모리 접근을 정확히 감지하고 적절히 처리하는 기능을 구현하는 것이 어려웠습니다. 이를 위해 명령어 및 데이터 메모리의 주소 범위를 엄격히 관리하였습니다.
3. 입출력 형식 맞추기
   - 출력 형식이 엄격하게 정해져 있어, 이를 정확히 맞추기 위해 많은 주의를 기울였습니다. 


****



# Project 1: RISC-V Binary Code Disassembler

## 💡 Project Introduction
RISC-V 바이너리 코드를 읽어 어셈블리 언어로 변환하는 프로그램을 개발하는 프로젝트. 주어진 바이너리 파일을 해독하여 어셈블리 코드로 출력.


## 🪄 Project Timeline
2022.10.01 ~ 2022.10.07


## 🎯 Functions
1. 바이너리 파일 읽기
   - 주어진 바이너리 파일을 읽어들여 RISC-V 명령어로 해석
2. 어셈블리 코드 출력
   - 각 명령어를 어셈블리 형식으로 변환하여 출력
   - 출력 형식: inst <instruction number>: <32-bit binary code in hex format> <disassembled instruction>
4. 명령어 해석
   - RISC-V 명령어 집합의 다양한 명령어를 해석
   - 지원되는 명령어: lui, auipc, jal, jalr, beq, bne, blt, bge, bltu, bgeu, lb, lh, lw, lbu, lhu, sb, sh, sw, addi, slti, sltiu, xori, ori, andi, slli, srli, srai, add, sub, sll, slt, sltu, xor, srl, sra, or, and

## 🚀 Program Execution
- 프로그램 이름: riscv-sim
- Python 파일의 경우: riscv-sim.py
- 실행 방법: `./riscv-sim <binary file>`


******


# Project 2: Single-cycle RISC-V CPU Simulator

## 💡 Project Introduction
RISC-V 명령어를 지원하는 단일 사이클 CPU 시뮬레이터를 구현하는 프로젝트. 
프로그램은 바이너리 파일에서 명령어를 읽어 하나씩 실행하며, 실행 후 레지스터의 현재 값을 출력합니다. 이 시뮬레이터는 실제 RISC-V 프로세서에서의 동작을 모방하여 레지스터 값이 예상 출력과 일치하는지 확인합니다.


## 🪄 Project Timeline
2022.11.01 ~ 2022.11.07


## 🎯 Functions
1. 명령어 실행
   - 주어진 바이너리 파일에서 명령어를 읽어와 하나씩 실행
   - 지원하는 RISC-V 명령어: lui, addi, slti, sltiu, xori, ori, andi, slli, srli, srai, add, sub, sll, slt, sltu, xor, srl, sra, or, and
2. 레지스터 초기화 및 출력
   - 모든 레지스터는 0으로 초기화 / x0 레지스터는 항상 0으로 고정
   - 명령어 실행 후 모든 레지스터의 현재 값을 출력


## 🚀 Program Execution
1. 명령어 실행
   - 프로그램 이름: riscv-sim
   - 실행 방법: `./riscv-sim <binary file> <number of instructions>` (예시: ./riscv-sim test1.bin 100)
2. 명령어 수에 따른 동작
   - 두 번째 인자로 주어진 명령어 수(N)만큼 실행
   - 만약 N이 입력 파일의 명령어 수보다 작으면, N개의 명령어를 실행하고 종료
   - 만약 N이 입력 파일의 명령어 수보다 크면, 모든 명령어를 실행하고 "No more instructions" 메시지를 출력한 후 종료
  

******


# Project 3: Single-cycle RISC-V CPU Simulator2

## 💡 Project Introduction
Project 2에서 구현한 단일 사이클 RISC-V CPU 시뮬레이터를 확장하여 더 많은 명령어를 지원하는 프로젝트.
추가된 명령어를 통해 보다 복잡한 프로그램을 실행할 수 있으며, 명령어 및 데이터 메모리의 오류 처리 기능을 포함합니다. 목표는 완전한 RISC-V 단일 사이클 CPU 시뮬레이터를 구현하는 것!


## 🪄 Project Timeline
2022.11.25 ~ 2022.12.02


## 🎯 Functions
1. 명령어 실행
   - Project 2에서 지원한 명령어와 더불어 다음 명령어들을 추가로 지원: auipc, jal, jalr, beq, bne, blt, bge, bltu, bgeu, lb, lh, lw, lbu, lhu, sb, sh, sw
2. 데이터 구조
   - 레지스터: x0 ~ x31 (x0은 항상 0)
      - 프로그램 카운터(PC): 0x00000000으로 초기화
      - 명령어 메모리: 주소 범위 0x00000000 ~ 0x0000FFFF (64KB)
      - 데이터 메모리: 주소 범위 0x10000000 ~ 0x1000FFFF (64KB)
3. 프로그램 실행
   - 프로그램은 2개 또는 3개의 command line argument를 받음
   - 두 개의 인수가 주어진 경우:
     - 첫 번째 인수: 명령어 바이너리 파일 이름
     - 두 번째 인수: 실행할 명령어의 수 (N)
   - 세 개의 인수가 주어진 경우:
     - 첫 번째 인수: 명령어 바이너리 파일 이름
     - 두 번째 인수: 데이터 바이너리 파일 이름
     - 세 번째 인수: 실행할 명령어의 수 (N)
4. 오류 처리
   - 유효하지 않은 메모리 주소 접근 시 "Memory address error" 메시지를 출력하고 종료
   - 지원하지 않는 명령어를 읽을 경우 "unknown instruction" 메시지를 출력하고 종료
5. 출력
   - 실행 후 모든 레지스터의 현재 값과 프로그램 카운터(PC)를 출력
  

## 🚀 Program Execution
- 프로그램 이름: riscv-sim
- 실행 방법:
  - 두 개의 인수를 사용하는 경우: `./riscv-sim <instruction file> <number of instructions>`
  - 세 개의 인수를 사용하는 경우: `./riscv-sim <instruction file> <data file> <number of instructions>`

