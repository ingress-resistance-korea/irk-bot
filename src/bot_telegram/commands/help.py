def get_documents(queue, update):
    docs = '`/help` 도움말을 출력해드려요.\n' \
           '`/intel` 원하는 장소의 인텔 스크린샷을 찍어드려요.\n' \
           '`/link` 레저네이터, 모드 상태에 따른 링크거리를 계산해드려요.\n' \
           '`/irk` 대한민국 레지스탕스 커뮤니티를 안내해드려요.\n' \
           '---------------------------------\n' \
           '*준비중인 기능 목록*\n' \
           '`/subscribe` 원하는 장소를 구독하여 특정 요일, 시간의 인텔 스크린샷을 제공해드려요. (준비중입니다)'
    update.message.reply_markdown(docs)
