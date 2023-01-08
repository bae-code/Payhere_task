# Payhere_task

## ERD

----
![erd](erd.png)

## API

----
<table style="border-collapse: collapse; width: 100%; height: 210px;" border="1" data-ke-align="alignLeft" data-ke-style="style12">
<tbody>
<tr style="height: 19px;">
<td style="width: 25%; text-align: center; height: 19px;">기능</td>
<td style="width: 25%; text-align: center; height: 19px;">Method</td>
<td style="width: 25%; height: 19px; text-align: center;">URL</td>
</tr>
<tr style="height: 17px;">
<td style="width: 25%; height: 17px;"><b>회원가입</b></td>
<td style="width: 25%; height: 17px;">POST</td>
<td style="width: 25%; height: 17px;">/user/register</td>
</tr>
<tr style="height: 19px;">
<td style="width: 25%; height: 19px;">로그인</td>
<td style="width: 25%; height: 19px;">POST</td>
<td style="width: 25%; height: 19px;">/user/login</td>
</tr>
<tr style="height: 17px;">
<td style="width: 25%; height: 17px;">로그아웃 </td>
<td style="width: 25%; height: 17px;">POST</td>
<td style="width: 25%; height: 17px;">/user/logout</td>
</tr>
<tr style="height: 17px;">
<td style="width: 25%; height: 17px;">가계부 작성</td>
<td style="width: 25%; height: 17px;">POST</td>
<td style="width: 25%; height: 17px;">/account-book/register</td>
</tr>
<tr style="height: 17px;">
<td style="width: 25%; height: 17px;">가계부 수정</td>
<td style="width: 25%; height: 17px;">PUT</td>
<td style="width: 25%; height: 17px;">/account-book/{pk}</td>
</tr>
<tr style="height: 17px;">
<td style="width: 25%; height: 17px;"><b>가계부 삭제</b></td>
<td style="width: 25%; height: 17px;">DELETE</td>
<td style="width: 25%; height: 17px;">/account-book/{pk}</td>
</tr>
<tr style="height: 17px;">
<td style="width: 25%; height: 17px;">가계부 리스트</td>
<td style="width: 25%; height: 17px;">POST</td>
<td style="width: 25%; height: 17px;">/account-book/list</td>
</tr>
<tr style="height: 17px;">
<td style="width: 25%; height: 17px;"><b>가계부 디테일</b></td>
<td style="width: 25%; height: 17px;">PUT</td>
<td style="width: 25%; height: 17px;">/account-book/{pk}</td>
</tr>
<tr style="height: 17px;">
<td style="width: 25%; height: 17px;"><b>가계부 복제</b></td>
<td style="width: 25%; height: 17px;">POST</td>
<td style="width: 25%; height: 17px;">/account-book/clone/{pk}</td>
</tr>
<tr style="height: 17px;">
<td style="width: 25%; height: 17px;">가계부 공유 URL 생성</td>
<td style="width: 25%; height: 17px;">GET</td>
<td style="width: 25%; height: 17px;">/account-book/share/{pk}</td>
</tr>
<tr style="height: 19px;">
<td style="width: 25%; height: 19px;">가계부 통계</td>
<td style="width: 25%; height: 19px;">GET</td>
<td style="width: 25%; height: 19px;">account-book/stat</td>
</tr>
</tbody>
</table>