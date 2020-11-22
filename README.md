# waffle-rookies-18.5-backend-2

현재 과제4 수행 중입니다. grace day 사용하려고 합니다. 과제 완료 후 며칠 사용했는지 추가하겠습니다.

=> 7일 사용하였습니다.

도메인 구입 비용을 환급받을 계좌 정보는 다음과 같습니다.
카카오뱅크 3333-15-9555347 정지민





시험이 끝난 지 얼마 지나지 않아서 아직 다 끝마치지 못했습니다. grace day 하루 사용하게 될 것 같습니다.





PUT /api/v1/seminar/{seminar_id}/
에서 request를 날린 user가 seminar의 instructor인지를 확인하는 code가 없었습니다. (user의 role만을 보고 판단)
즉, 해당 seminar의 instructor가 아닌 user라도 role이 instructor기만 하면 PUT /api/v1/seminar/{seminar_id}/를 통해 seminar 정보를 수정할 수 있었습니다.
