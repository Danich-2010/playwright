Загрузки
Введение
Для каждого загруженного на страницу вложения генерируется событие page.on("download") . Все эти вложения загружаются во временную папку. Вы можете получить URL-адрес загрузки, имя файла и поток данных, используя объект Download из события.

Вы можете указать, куда сохранять загруженные файлы, используя параметр downloads_path в функции browser_type.launch() .

примечание
Загруженные файлы удаляются при закрытии контекста браузера, который их создал.

Вот самый простой способ осуществить загрузку файла:

Синхронизация
Асинхронный
# Start waiting for the download
with page.expect_download() as download_info:
    # Perform the action that initiates download
    page.get_by_text("Download file").click()
download = download_info.value

# Wait for the download process to complete and save the downloaded file somewhere
download.save_as("/path/to/save/at/" + download.suggested_filename)

Варианты
Если вы понятия не имеете, что инициирует загрузку, вы все равно можете обработать это событие:

Синхронизация
Асинхронный
page.on("download", lambda download: print(download.path()))

Обратите внимание, что обработка события разветвляет поток управления и затрудняет отслеживание сценария. Ваш сценарий может завершиться во время загрузки файла, поскольку основной поток управления не ожидает завершения этой операции.

примечание
Инструкции по загрузке файлов см. в разделе «Загрузка файлов» .