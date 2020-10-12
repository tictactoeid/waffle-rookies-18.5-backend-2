# waffle-rookies-18.5-backend-2

시험이 끝난 지 얼마 지나지 않아서 아직 다 끝마치지 못했습니다. grace day 하루 사용하게 될 것 같습니다.





```
PUT /api/v1/seminar/{seminar_id}/
```
에서 request를 날린 user가 seminar의 instructor인지를 확인하는 code가 없었습니다. (user의 role만을 보고 판단)
즉, 해당 seminar의 instructor가 아닌 user라도 role이 instructor기만 하면 PUT /api/v1/seminar/{seminar_id}/를 통해 seminar 정보를 수정할 수 있었습니다.

```
DELETE /api/v1/seminar/{seminar_id}/user/
```
에서 실제로 seminar에 참여 중이 아닌 user (role은 participant)가 delete request를 날렸을 때
```Python
userseminar = UserSeminar.objects.get(user=user, seminar=seminar)
```
이 부분을 ```try:```문으로 잡지 않아서 오류가 발생했습니다. 실제였다면 아마 ```500 Interal Server Error```가 발생할 상황이었겠지요. 현재는 해결해서 ```403 Forbidden```을 return하도록 바꾸었습니다.

```
POST, DELETE /api/v1/seminar/{seminar_id}/user/
```
에서, 같은 url을 사용하는 두 api가 있습니다.

https://github.com/wafflestudio/rookies/issues/207
와 같은 상황이 발생하여, 

```Python
    @action(methods=['POST', 'DELETE'], detail=True, url_path = 'user', url_name='user') # POST, DELETE /api/v1/seminar/{seminar_id}/user/
    def user(self, request, pk=None):
        if self.request.method == 'POST':
            return self.participate(request, pk)
        elif self.request.method == 'DELETE':
            return self.drop(request, pk)
        else:
            return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
 ```
와 같은 코드를 추가하고 기존의 ```@action``` decorator를   해결했습니다.
