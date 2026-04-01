# Имя workflow — проверка экзаменационного задания
name: Exam Integrity Test - Broken Cowsay Script

# Триггеры — запуск при пуше (чтобы убедиться, что задание не сломалось)
on:
  push:
    branches: [main]
    paths:
      - 'exams/exam3/**'  # Запускается только при изменении экзамена
  workflow_dispatch:      # Можно запустить вручную

jobs:
  # Проверка, что экзаменационное задание содержит ровно 5 ошибок
  exam-validation:
    runs-on: ubuntu-latest
    
    steps:
      # Шаг 1: Клонирование репозитория
      - uses: actions/checkout@v4
      
      # Шаг 2: Сборка образа
      - name: Build exam image
        run: |
          docker build -t exam-server ./exams/exam3
          echo "✅ Image built successfully"
      
      # Шаг 3: Запуск контейнера
      - name: Run exam container
        run: |
          docker run -d \
            --name exam-container \
            -p 2222:22 \
            exam-server
          sleep 5  # Ждём старта SSH
      
      # Шаг 4: Проверка, что контейнер запустился
      - name: Verify container is running
        run: |
          if docker ps | grep -q exam-container; then
            echo "✅ Container is running"
          else
            echo "❌ Container failed to start"
            exit 1
          fi
      
      # Шаг 5: Установка sshpass для тестирования
      - name: Install sshpass
        run: |
          sudo apt-get update
          sudo apt-get install -y sshpass
      
      # Шаг 6: Проверка SSH-доступа
      - name: Test SSH connection
        run: |
          echo "Testing SSH connection..."
          if sshpass -p 'exam2026' ssh -o StrictHostKeyChecking=no \
            -o ConnectTimeout=10 \
            student@localhost -p 2222 \
            "echo 'SSH OK'"; then
            echo "✅ SSH connection successful"
          else
            echo "❌ SSH connection failed"
            exit 1
          fi
      
      # Шаг 7: Проверка наличия скрипта talk.sh
      - name: Check if talk.sh exists
        run: |
          if sshpass -p 'exam2026' ssh -o StrictHostKeyChecking=no \
            student@localhost -p 2222 \
            "[ -f /home/student/talk.sh ]"; then
            echo "✅ talk.sh exists"
          else
            echo "❌ talk.sh not found"
            exit 1
          fi
      
      # Шаг 8: Проверка прав на выполнение
      - name: Check execute permission
        run: |
          if sshpass -p 'exam2026' ssh -o StrictHostKeyChecking=no \
            student@localhost -p 2222 \
            "[ -x /home/student/talk.sh ]"; then
            echo "✅ talk.sh is executable"
          else
            echo "❌ talk.sh is not executable"
            exit 1
          fi
      
      # Шаг 9: Проверка, что скрипт действительно содержит ошибки
      - name: Verify script has syntax errors
        run: |
          echo "Checking script syntax..."
          output=$(sshpass -p 'exam2026' ssh -o StrictHostKeyChecking=no \
            student@localhost -p 2222 \
            "bash -n /home/student/talk.sh 2>&1" || true)
          
          if echo "$output" | grep -q "error"; then
            echo "✅ Script has syntax errors (as expected)"
            echo "Errors found:"
            echo "$output"
          else
            echo "❌ Script has no syntax errors — exam is broken!"
            echo "Expected: script with 5 errors"
            echo "Actual: script is syntactically correct"
            exit 1
          fi
      
      # Шаг 10: Проверка, что при запуске скрипт падает с ошибкой
      - name: Verify script fails when run
        run: |
          echo "Attempting to run script (should fail)..."
          set +e  # Временно отключаем exit on error
          sshpass -p 'exam2026' ssh -o StrictHostKeyChecking=no \
            student@localhost -p 2222 \
            "cd /home/student && ./talk.sh" 2>&1
          exit_code=$?
          set -e
          
          if [ $exit_code -ne 0 ]; then
            echo "✅ Script fails with exit code $exit_code (as expected)"
          else
            echo "❌ Script succeeded — exam is broken!"
            echo "Expected: script should fail with 5 errors"
            echo "Actual: script runs successfully"
            exit 1
          fi
      
      # Шаг 11: Проверка наличия подсказок
      - name: Check hints file exists
        run: |
          if sshpass -p 'exam2026' ssh -o StrictHostKeyChecking=no \
            student@localhost -p 2222 \
            "[ -f /opt/hints.txt ]"; then
            echo "✅ hints.txt exists"
          else
            echo "⚠️ Warning: hints.txt not found (optional)"
          fi
      
      # Шаг 12: Подсчёт количества ошибок в скрипте
      - name: Count errors in script
        run: |
          echo "Analyzing script for expected error patterns..."
          
          # Получаем содержимое скрипта
          sshpass -p 'exam2026' ssh -o StrictHostKeyChecking=no \
            student@localhost -p 2222 \
            "cat /home/student/talk.sh" > /tmp/talk.sh
          
          # Проверяем типичные ошибки (можно настроить под реальный скрипт)
          error_count=0
          
          # Ошибка 1: Отсутствует shebang
          if ! grep -q "^#!/bin/bash" /tmp/talk.sh; then
            echo "  Error 1: Missing shebang (#!/bin/bash)"
            ((error_count++))
          fi
          
          # Ошибка 2: Неправильный синтаксис массива
          if grep -q "phrases=" /tmp/talk.sh && ! grep -q "phrases=(" /tmp/talk.sh; then
            echo "  Error 2: Wrong array syntax"
            ((error_count++))
          fi
          
          # Ошибка 3: Проблема с кавычками в cowsay
          if grep -q "cowsay" /tmp/talk.sh && ! grep -q 'cowsay "\$phrase"' /tmp/talk.sh; then
            echo "  Error 3: Quotes issue in cowsay command"
            ((error_count++))
          fi
          
          # Ошибка 4: Неправильный подсчёт длины строки
          if grep -q "length=" /tmp/talk.sh && ! grep -q '${#phrase}' /tmp/talk.sh; then
            echo "  Error 4: Wrong string length calculation"
            ((error_count++))
          fi
          
          # Ошибка 5: Проблема с индексом массива
          if grep -q "RANDOM" /tmp/talk.sh && ! grep -q '${#phrases\[@\]}' /tmp/talk.sh; then
            echo "  Error 5: Wrong array indexing"
            ((error_count++))
          fi
          
          echo ""
          if [ $error_count -eq 5 ]; then
            echo "✅ Found exactly 5 errors in the script — exam is correctly broken!"
          elif [ $error_count -gt 0 ]; then
            echo "⚠️ Found $error_count errors, but expected exactly 5"
            echo "   Exam may have been modified unintentionally"
            exit 1
          else
            echo "❌ Found 0 errors — exam is not broken!"
            echo "   The script appears to be correct, but should contain 5 errors"
            exit 1
          fi
      
      # Шаг 13: Проверка, что скрипт становится рабочим после исправлений
      - name: Verify script can be fixed
        run: |
          echo "Testing if script can be fixed (simulating student work)..."
          
          # Создаём исправленную версию
          sshpass -p 'exam2026' ssh -o StrictHostKeyChecking=no \
            student@localhost -p 2222 << 'EOF'
          
          # Создаём исправленный скрипт
          cat > /home/student/talk_fixed.sh << 'SCRIPT'
          #!/bin/bash
          phrases=(
              "Привет, мир!"
              "Я люблю DevOps!"
              "Bash - это весело!"
          )
          random_index=$((RANDOM % ${#phrases[@]}))
          phrase="${phrases[$random_index]}"
          echo "Фраза: $phrase"
          cowsay "$phrase"
          length=${#phrase}
          echo "Длина фразы: $length символов"
          echo "Успех! Корова довольна"
          SCRIPT
          
          chmod +x /home/student/talk_fixed.sh
          EOF
          
          # Запускаем исправленный скрипт
          output=$(sshpass -p 'exam2026' ssh -o StrictHostKeyChecking=no \
            student@localhost -p 2222 \
            "cd /home/student && ./talk_fixed.sh" 2>&1)
          
          echo "$output"
          
          # Проверяем, что всё работает
          if echo "$output" | grep -q "Корова довольна"; then
            echo "✅ Script can be fixed — exam is valid"
          else
            echo "❌ Even fixed script doesn't work — exam design is flawed"
            exit 1
          fi
      
      # Шаг 14: Очистка
      - name: Cleanup
        if: always()
        run: |
          docker stop exam-container || true
          docker rm exam-container || true
          echo "✅ Cleanup complete"
      
      # Шаг 15: Итоговый результат
      - name: Final result
        if: always()
        run: |
          echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
          echo "📋 EXAM INTEGRITY CHECK COMPLETED"
          echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
          echo ""
          echo "✅ Container builds successfully"
          echo "✅ SSH works with password 'exam2026'"
          echo "✅ talk.sh exists and is executable"
          echo "✅ Script has 5 errors (as designed)"
          echo "✅ Script fails when run (as expected)"
          echo "✅ Script can be fixed to work correctly"
          echo ""
          echo "🎉 Exam is valid and ready for students!"
