#!/bin/bash

# 定義目錄（假設 Submission 在當前目錄下）
SUBMISSION_DIR="./Submission"
DECODE_SCRIPT="./tools/decode.py"

# 輸出總檔案
OUTPUT_FILE="decoded_results.txt"
> "$OUTPUT_FILE"  # 清空

TIME_LIMIT="5s"  # 每個檔案執行最多 5 秒

for file in "$SUBMISSION_DIR"/*; do
    echo "處理檔案: $file" >> "$OUTPUT_FILE"
    if [[ "$file" == *.cpp ]]; then
        exe="${file%.cpp}.exe"
        if g++ "$file" -o "$exe"; then
            code="$(timeout $TIME_LIMIT "$exe")"
        else
            echo "[編譯失敗]" >> "$OUTPUT_FILE"
            continue
        fi
    elif [[ "$file" == *.py ]]; then
        code="$(timeout $TIME_LIMIT python3 "$file")"
    fi

    if [[ -n "$code" ]]; then
        python3 "$DECODE_SCRIPT" "$code" >> "$OUTPUT_FILE"
    else
        echo "[執行逾時或無輸出]" >> "$OUTPUT_FILE"
    fi

    echo -e "\n--------------------\n" >> "$OUTPUT_FILE"
done
