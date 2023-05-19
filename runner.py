import argparse
import json
import os
from typing import Dict

from engine import IngterpreterEngine


# 가능한 명령어
__ALLOWED_COMMANDS = ("install", "uninstall", "run", "convert")

# 언어 설정 파일 필수 키들
__FIRST_KEYS = ("TITLE", "EXT", "COMMANDS")
__SECOND_KEYS = ("COMMANDS/ACTIVATION", "COMMANDS/OPERATION")
__THIRD_KEYS = (
    "COMMANDS/ACTIVATION/START", 
    "COMMANDS/ACTIVATION/END", 
    "COMMANDS/OPERATION/INC_PTR_OP", 
    "COMMANDS/OPERATION/DEC_PTR_OP",
    "COMMANDS/OPERATION/INC_VAL_OP", 
    "COMMANDS/OPERATION/DEC_VAL_OP",
    "COMMANDS/OPERATION/PRINT_OP", 
    "COMMANDS/OPERATION/STORE_OP",
    "COMMANDS/OPERATION/LOOP_BEGIN_OP", 
    "COMMANDS/OPERATION/LOOP_END_OP"
)


def validate_configuration(cfg_dict:Dict):
    missing_keys = list()
    for k in __FIRST_KEYS:
        if k not in cfg_dict:
            # 1단계 필수 키가 없쪙
            missing_keys.append(k)
    for k in __SECOND_KEYS:
        pk, ck = k.split('/')
        if pk in missing_keys or ck not in cfg_dict[pk]:
            # 2단계 필수 키가 없쪙
            missing_keys.append(k)
    for k in __THIRD_KEYS:
        p1k, p2k, ck = k.split('/')
        if p1k in missing_keys or f"{p1k}/{p2k}" in missing_keys \
            or ck not in cfg_dict[p1k][p2k]:
            # 3단계 필수 키가 없쪙
            missing_keys.append(k)
        elif ck in ("LOOP_BEGIN_OP", "LOOP_END_OP"):
            # "LOOP_BEGIN_OP", "LOOP_END_OP"는 한 글자만 할당 가능
            if len(cfg_dict[p1k][p2k][ck]) != 1:
                # 3단계 필수 키가 잘못 설정됐쪙
                missing_keys.append(k)
        else:
            if len(cfg_dict[p1k][p2k][ck]) < 1:
                # 3단계 필수 키가 잘못 설정됐쪙
                missing_keys.append(k)
    
    return len(missing_keys), missing_keys


def register_ingterpreter_alias(lang_name:str):
    home_dir = os.path.expanduser("~")
    shell = os.environ.get("SHELL", "")
    lang_name = lang_name.strip()
    
    # BASH와 ZSH 쉘을 지원.
    if "bash" in shell.lower():
        profile_file = os.path.join(home_dir, ".bashrc")
    elif "zsh" in shell.lower():
        profile_file = os.path.join(home_dir, ".zshrc")
    else:
        raise EnvironmentError("error: supports either `bash` or `zsh` shell env.\n\t"
            f"{shell} is unsupported")

    # 쉘 명령어 alias 등록
    with open(profile_file, 'a') as f:
        f.write(f"\nalias {lang_name}='python engine.py {lang_name}'\n")


def remove_ingterpreter_alias(lang_name:str):
    home_dir = os.path.expanduser("~")
    shell = os.environ.get("SHELL", "")
    lang_name = lang_name.strip()
    
    # BASH와 ZSH 쉘을 지원.
    if "bash" in shell.lower():
        profile_file = os.path.join(home_dir, ".bashrc")
    elif "zsh" in shell.lower():
        profile_file = os.path.join(home_dir, ".zshrc")
    else:
        print("warning: supports either `bash` or `zsh` shell env.\n\t"
            f"{shell} is unsupported")
        return

    # 쉘 명령어 alias 등록 해제
    with open(profile_file, 'r') as f:
        lines = f.readlines()
    with open(profile_file, 'w') as f:
        for line in lines:
            if f"alias {lang_name}" not in line:
                f.write(line)
            else:
                print(f"deleted '{line}' from `{profile_file}`.")


if __name__ == "__main__":
    KNOWN_CONFIGS = [ f.replace(".json", '') for f in os.listdir("configs/") if ".json" in f ]
    ALLOWED_COMMANDS = list(__ALLOWED_COMMANDS) + KNOWN_CONFIGS
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs=1, choices=ALLOWED_COMMANDS) 
    parser.add_argument("arguments", nargs='*')
    try:
        args = parser.parse_args()

        assert len(args.command)!=0
        assert len(args.arguments)>=1
        if args.command[0] in KNOWN_CONFIGS:
            # `<LANG_NAME> <COMMAND> <...>`
            args.lang_name = args.command[0].strip()
            args.command = args.arguments.pop(0)
        elif args.arguments[0] in KNOWN_CONFIGS:
            # `python runner.py <COMMAND> <LANG_NAME> <...>`
            args.lang_name = args.arguments.pop(0).strip()
            args.command = args.command[0]
        else: raise AssertionError
        assert args.command in __ALLOWED_COMMANDS
    except:
        raise AssertionError("error: a valid command is required\n\t"
            f"`<LANG_NAME> <COMMAND> <...>`, where `<COMMAND>` is one of {__ALLOWED_COMMANDS}"
            f"or `python runner.py <COMMAND> <LANG_NAME> <...>`, where `<COMMAND>` is one of {__ALLOWED_COMMANDS}")
    
    # 삭제
    if args.command == "uninstall":
        # alias를 시스템에 등록 해제
        remove_ingterpreter_alias(args.lang_name)
        print(f"your Ingterpreter-based language \"{args.lang_name}\" is uninstalled!")

    else:
        # install / convert / run 공통
        if not os.path.isfile(f"configs/{args.lang_name}.json"):
            # 파일이 없쪙
            raise FileNotFoundError("error: valid language configuration file is required\n\t"
                f"please check if {args.lang_name}.json exists under the configs/ folder.")
        with open(f"configs/{args.lang_name}.json", 'r', encoding="utf-8") as j:
            CFG = json.load(j)
            # JSON 언어 설정 파일에 필수 키들이 모두 있는지 확인
            ERROR_CODE, MISSING_KEYS = validate_configuration(CFG)
            assert ERROR_CODE == 0, ("error: valid language configuration file is required\n\t"
                f"please check if following keys have valid values: {MISSING_KEYS}")

        # 설치
        if args.command == "install":
            # alias를 시스템에 등록
            register_ingterpreter_alias(args.lang_name)
            print(f"your Ingterpreter-based language \"{args.lang_name}\" is registered!")

        # 코드 변환
        elif args.command == "convert":
            ING = IngterpreterEngine(CFG)

        # 코드 실행
        else: # if args.command == "run":
            ING = IngterpreterEngine(CFG)
