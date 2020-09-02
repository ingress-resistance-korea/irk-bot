# irk-event-worker
message queue worker

# features

### realtime request
- request with location name
- get realtime intel screenshot

### map subscribe
- register specific location name and time
- get scheduled intel screenshot

# specification

#### sample request data
```json
{
	"event_id": "b45f5fa6-f0aa-448b-baa0-f684f4a97c44",
	"response_event_to": "intel_response_telegram",
	"location": "seoul station",
	"chat": {
		"id": 1111111111,
		"type": "private",
		"username": "XXXXX",
		"first_name": "XXXXX"
	},
	"message": {
		"message_id": 111,
		"date": 11111111,
		"chat": {
			"id": 11111111111,
			"type": "private",
			"username": "XXXXX",
			"first_name": "XXXXX"
		},
		"text": "/intel seoul station",
		"entities": [
			{
				"type": "bot_command",
				"offset": 0,
				"length": 6
			}
		],
		"caption_entities": [],
		"photo": [],
		"new_chat_members": [],
		"new_chat_photo": [],
		"delete_chat_photo": false,
		"group_chat_created": false,
		"supergroup_chat_created": false,
		"channel_chat_created": false,
		"from": {
			"id": 111111111,
		    "first_name": "XXXXX🇷",
			"is_bot": false,
			"username": "XXXXX",
			"language_code": "ab"
		}
	},
	"user": {
		"id": 11111111,
		"first_name": "XXXXX",
		"is_bot": false,
		"username": "XXXXX",
		"language_code": "ko"
	}
}
```

#### sample response data
```json
{
	"event_id": "e8e1a3f5-2ecd-4d80-9102-5e47754788d6",
	"result": {
		"success": true,
		"url": "https://XXXXXXXX.XXX/screenshots/20200903005728.jpg",
		"address": "Seoul Station, 43-205 Dongja-dong, Yongsan-gu, Seoul, South Korea",
		"error_message": [
			null
		],
		"timestamp": "2020-09-03 00:57:28.366038"
	},
	"chat": {
		"id": 11111,
		"type": "private",
		"username": "XXXXX",
		"first_name": "XXXXX"
	},
	"message": {
		"message_id": 330,
		"date": 11111,
		"chat": {
			"id": 11111,
			"type": "private",
			"username": "XXXXX",
			"first_name": "XXXXX"
		},
		"text": "/intel 서울역",
		"entities": [
			{
				"type": "bot_command",
				"offset": 0,
				"length": 6
			}
		],
		"caption_entities": [],
		"photo": [],
		"new_chat_members": [],
		"new_chat_photo": [],
		"delete_chat_photo": false,
		"group_chat_created": false,
		"supergroup_chat_created": false,
		"channel_chat_created": false,
		"from": {
			"id": 11111,
			"first_name": "XXXXX",
			"is_bot": false,
			"username": "XXXXX",
			"language_code": "ab"
		}
	},
	"user": {
		"id": 11111,
		"first_name": "XXXXX",
		"is_bot": false,
		"username": "XXXXX",
		"language_code": "ko"
	}
}
````