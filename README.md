# waffle-rookies-18.5-backend-2

시험이 끝난 지 얼마 지나지 않아서 아직 다 끝마치지 못했습니다. grace day 하루 사용하게 될 것 같습니다.





PUT /api/v1/seminar/{seminar_id}/
에서 request를 날린 user가 seminar의 instructor인지를 확인하는 code가 없었습니다. (user의 role만을 보고 판단)
즉, 해당 seminar의 instructor가 아닌 user라도 role이 instructor기만 하면 PUT /api/v1/seminar/{seminar_id}/를 통해 seminar 정보를 수정할 수 있었습니다.
