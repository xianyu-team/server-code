# API
XianYux闲余挣闲钱系统API文档

- [API](#api)
- [服务器IP和端口号](#%E6%9C%8D%E5%8A%A1%E5%99%A8ip%E5%92%8C%E7%AB%AF%E5%8F%A3%E5%8F%B7)
- [Session](#session)
- [手机短信](#%E6%89%8B%E6%9C%BA%E7%9F%AD%E4%BF%A1)
  - [获取手机验证码](#%E8%8E%B7%E5%8F%96%E6%89%8B%E6%9C%BA%E9%AA%8C%E8%AF%81%E7%A0%81)
  - [验证手机验证码](#%E9%AA%8C%E8%AF%81%E6%89%8B%E6%9C%BA%E9%AA%8C%E8%AF%81%E7%A0%81)
- [用户](#%E7%94%A8%E6%88%B7)
  - [用户注册](#%E7%94%A8%E6%88%B7%E6%B3%A8%E5%86%8C)
  - [完善或修改个人信息](#%E5%AE%8C%E5%96%84%E6%88%96%E4%BF%AE%E6%94%B9%E4%B8%AA%E4%BA%BA%E4%BF%A1%E6%81%AF)
  - [获取个人信息](#%E8%8E%B7%E5%8F%96%E4%B8%AA%E4%BA%BA%E4%BF%A1%E6%81%AF)
  - [用户密码登录](#%E7%94%A8%E6%88%B7%E5%AF%86%E7%A0%81%E7%99%BB%E5%BD%95)
  - [找回密码-重置密码](#%E6%89%BE%E5%9B%9E%E5%AF%86%E7%A0%81-%E9%87%8D%E7%BD%AE%E5%AF%86%E7%A0%81)
  - [用户短信登录](#%E7%94%A8%E6%88%B7%E7%9F%AD%E4%BF%A1%E7%99%BB%E5%BD%95)
  - [用户退出登录](#%E7%94%A8%E6%88%B7%E9%80%80%E5%87%BA%E7%99%BB%E5%BD%95)
  - [获取当前用户的余额](#%E8%8E%B7%E5%8F%96%E5%BD%93%E5%89%8D%E7%94%A8%E6%88%B7%E7%9A%84%E4%BD%99%E9%A2%9D)
  - [获得当前用户发布/领取的任务列表](#%E8%8E%B7%E5%BE%97%E5%BD%93%E5%89%8D%E7%94%A8%E6%88%B7%E5%8F%91%E5%B8%83%E9%A2%86%E5%8F%96%E7%9A%84%E4%BB%BB%E5%8A%A1%E5%88%97%E8%A1%A8)
  - [根据用户id获取个人信息](#%E6%A0%B9%E6%8D%AE%E7%94%A8%E6%88%B7id%E8%8E%B7%E5%8F%96%E4%B8%AA%E4%BA%BA%E4%BF%A1%E6%81%AF)
  - [获取当前用户的关注列表](#%E8%8E%B7%E5%8F%96%E5%BD%93%E5%89%8D%E7%94%A8%E6%88%B7%E7%9A%84%E5%85%B3%E6%B3%A8%E5%88%97%E8%A1%A8)
  - [获取当前用户的粉丝列表](#%E8%8E%B7%E5%8F%96%E5%BD%93%E5%89%8D%E7%94%A8%E6%88%B7%E7%9A%84%E7%B2%89%E4%B8%9D%E5%88%97%E8%A1%A8)
- [任务](#%E4%BB%BB%E5%8A%A1)
  - [获取任务大厅的任务列表](#%E8%8E%B7%E5%8F%96%E4%BB%BB%E5%8A%A1%E5%A4%A7%E5%8E%85%E7%9A%84%E4%BB%BB%E5%8A%A1%E5%88%97%E8%A1%A8)
  - [根据任务id获取拿快递和外卖的详细信息](#%E6%A0%B9%E6%8D%AE%E4%BB%BB%E5%8A%A1id%E8%8E%B7%E5%8F%96%E6%8B%BF%E5%BF%AB%E9%80%92%E5%92%8C%E5%A4%96%E5%8D%96%E7%9A%84%E8%AF%A6%E7%BB%86%E4%BF%A1%E6%81%AF)
  - [根据任务id获取问卷的详细信息](#%E6%A0%B9%E6%8D%AE%E4%BB%BB%E5%8A%A1id%E8%8E%B7%E5%8F%96%E9%97%AE%E5%8D%B7%E7%9A%84%E8%AF%A6%E7%BB%86%E4%BF%A1%E6%81%AF)
  - [根据问卷id获取问卷的所有题目的详细信息](#%E6%A0%B9%E6%8D%AE%E9%97%AE%E5%8D%B7id%E8%8E%B7%E5%8F%96%E9%97%AE%E5%8D%B7%E7%9A%84%E6%89%80%E6%9C%89%E9%A2%98%E7%9B%AE%E7%9A%84%E8%AF%A6%E7%BB%86%E4%BF%A1%E6%81%AF)
  - [接受任务](#%E6%8E%A5%E5%8F%97%E4%BB%BB%E5%8A%A1)
  - [完成任务](#%E5%AE%8C%E6%88%90%E4%BB%BB%E5%8A%A1)
  - [取消发布任务](#%E5%8F%96%E6%B6%88%E5%8F%91%E5%B8%83%E4%BB%BB%E5%8A%A1)
  - [新建任务](#%E6%96%B0%E5%BB%BA%E4%BB%BB%E5%8A%A1)
  - [新建一个拿快递和外卖的任务](#%E6%96%B0%E5%BB%BA%E4%B8%80%E4%B8%AA%E6%8B%BF%E5%BF%AB%E9%80%92%E5%92%8C%E5%A4%96%E5%8D%96%E7%9A%84%E4%BB%BB%E5%8A%A1)
  - [新建一个问卷任务](#%E6%96%B0%E5%BB%BA%E4%B8%80%E4%B8%AA%E9%97%AE%E5%8D%B7%E4%BB%BB%E5%8A%A1)
- [账单](#%E8%B4%A6%E5%8D%95)
  - [新增当前用户的交易记录](#%E6%96%B0%E5%A2%9E%E5%BD%93%E5%89%8D%E7%94%A8%E6%88%B7%E7%9A%84%E4%BA%A4%E6%98%93%E8%AE%B0%E5%BD%95)
  - [获取当前用户的交易历史](#%E8%8E%B7%E5%8F%96%E5%BD%93%E5%89%8D%E7%94%A8%E6%88%B7%E7%9A%84%E4%BA%A4%E6%98%93%E5%8E%86%E5%8F%B2)
  - [当前用户的闲余币充值](#%E5%BD%93%E5%89%8D%E7%94%A8%E6%88%B7%E7%9A%84%E9%97%B2%E4%BD%99%E5%B8%81%E5%85%85%E5%80%BC)

# 服务器IP和端口号
- IP : 120.77.146.251
- Port : 8000



# Session

* 用户id: request.session['user_id']
* 登录状态: request.session['login']



# 手机短信


## 获取手机验证码
> `GET /sms/verification_code`

**参数**
```
{
    "user_phone":    "string"    //手机号
}
```

**返回值**

```
{
    "code":                 integer,     //状态码
    "message":              "string",    //信息
    "verification_code":    "string"     //手机验证码
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK",
    "verification_code": "5128"
}
```
- 400
```
    "code": 400,
    "message": "无效的手机号"  //该手机号已经被注册（备选）
                              //服务器发生错误（备选）
```


## 验证手机验证码
> `POST /sms/verification`

**参数**
```
{
    "user_phone":           "string",    //手机号
    "verification_code":    "string"     //验证码
}
```

**返回值**
```
{
    "code":       integer,     //状态码
    "message":    "string"     //信息
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK"
}
```
- 400
```
    "code": 400,
    "message": "手机验证码错误"  //服务器发生错误（备选）
```


# 用户

## 用户注册
> `POST /user`

**参数**

```
{
    "user_phone":       "string",    //手机号
    "user_password":    "string"     //密码
}
```

**返回值**
```
{
    "code":       integer,    //状态码
    "message":    "string"    //信息
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK"
}
```
- 400
```
    "code": 400,
    "message": "该手机号已经被注册"  //服务器发生错误（备选）
```


## 完善或修改个人信息
> `PUT /user/profile`

**参数**
```
{
    "user_icon":              "string",    //头像，图片的byte数组转成字符串
    "student_name":           "string",    //真实姓名
    "student_university":     "string",    //学校
    "student_academy":        "string",    //学院
    "student_number":         "string",    //学号
    "student_gender":         integer      //性别，0为女，1为男
}
```

**返回值**
```
{
    "code":       integer,     //状态码
    "message":    "string"    //信息
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK"
}
```
- 400
```
    "code": 400,
    "message": "服务器发生错误"  
```

* 401

```
    "code": 401,
    "message": "用户未登录"
```



## 获取个人信息

> `GET /user/profile`

**参数**
```
{
    无
}
```

**返回值**
```
{
    "code":                   integer,     //状态码
    "message":                "string",    //信息
    "user_phone":             "string",    //手机号
    "user_icon":              "string",    //头像，图片的byte数组转成字符串
    "student_name":           "string",    //真实姓名
    "student_university":     "string",    //学校
    "student_academy":        "string",    //学院
    "student_number":         "string",    //学号
    "student_gender":         integer      //性别，0为女，1为男
}
```

**返回示例**
- 200
```
    "code": 200,
    "message": "OK,
    "user_phone": "15988991556",
    "user_icon": "x\86\45...",    
    "student_name": "张三",   
    "student_university": "中山大学", 
    "student_academy": "数据科学与计算机学院",    
    "student_number": "16330033",   
    "student_sex": 0
```
- 400
```
    "code": 400,
    "message": "服务器发生错误"
```

- 401

```
    "code": 401,
    "message": "用户未登录"
```

## 用户密码登录

> `POST /user/password/session`

**参数**

```
{
    "user_phone":       "string",    //手机号
    "user_password":    "string"     //密码
}
```

**返回值**

```
{
    "code":          integer,     //状态码
    "message":       "string",    //信息
    "user_fillln"    integer      //用户是否完善了个人信息，0为否，1为是
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK",
    "user_fillln": 0
}
```
- 400
```
    "code": 400,
    "message": "用户名不存在"  //密码错误（备选）
                              //服务器发生错误（备选）
```

- 401

```
    "code": 401,
    "message": "用户未登录"
```


## 找回密码-重置密码

> `PUT /user/password`

**参数**
```
{
    "user_phone":            "string",
    "user_password":         "string",
     "verification_code":    "string"     //参数增加手机验证码，为了防止密码被他人修改而不是本人修改
}
```

**返回值**
```
{
    "code":       integer,     //状态码
    "message":    "string"     //信息
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK"
}
```
- 400
```
    "code": 400,
    "message": "手机验证码错误"  //服务器发生错误（备选）
```


## 用户短信登录

> `POST /user/sms/session`

**参数**
```
{
    "user_phone":           "string",    //手机号
    "verification_code":    "string"     //验证码
}
```

**返回值**
```
{
    "code":          integer,     //状态码
    "message":       "string",    //信息
    "user_fillln"    integer      //用户是否完善了个人信息，0为否，1为是
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK"
    "user_fillln": 0
}
```
- 400
```
    "code": 400,
    "message": "手机验证码错误"  //服务器发生错误（备选）
```


## 用户退出登录
> `DELETE /user/session`

**参数**
```
无
```

**返回值**
```
{
    "code":       integer,     //状态码
    "message":    "string"     //信息
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK"
}
```
- 400
```
    "code": 400,
    "message": "服务器发生错误"
```

- 401

```
    "code": 401,
    "message": "用户未登录"
```


## 获取当前用户的余额
> `GET /user/balance`

**参数**
```
无
```

**返回值**
```
{
    "code":            integer,     //状态码
    "message":         "string",    //信息
    "user_balance":    integer      //用户闲余币
}
```

**返回示例**

- 200
```
{
    "code": 200,
    "message": "OK",
    "user_balance": 100
}
```
- 400
```
    "code": 400,
    "message": "服务器发生错误"
```

- 401

```
    "code": 401,
    "message": "用户未登录"
```


## 获得当前用户发布/领取的任务列表

> `GET /user/tasks`

**参数**	

```
{

}
```

**返回值**

```
{
   
}
```

**返回示例**

- 200
```
{
    
}
```
- 400
```
    "code": 400,
    "message": "服务器发生错误"
```

- 401

```
    "code": 401,
    "message": "用户未登录"
```





## 根据用户id获取个人信息

> `GET /user/information`


**参数**

```
{
    "user_ids":  [
        {
            "user_id":    integer    //用户id
        }
    ]
}
```

**返回值**

```
{
    "code":                           integer,     //状态码
    "message":                        "string",    //信息
    "users": [
        {
            "user_phone":             "string",    //手机号
            "user_icon":              "string",    //头像，图片的byte数组转成字符串
            "student_name":           "string",    //真实姓名
            "student_university":     "string",    //学校
            "student_academy":        "string",    //学院
            "student_number":         "string",    //学号
            "student_gender":         integer      //性别，0为女，1为男
        }
    ]
}
```

**返回示例**

- 200

```
{
    "code": 200,
    "message": "OK",
    "users": [
        {
            //省略...
        }
    ]
}
```

- 400

```
    "code": 400,
    "message": "服务器发生错误"
```

- 401

```
    "code": 401,
    "message": "用户未登录"
```



## 获取当前用户的关注列表

> `GET /user/followings`

**参数**
```
无
```

**返回值**

```
{
    "code":             integer,     //状态码
    "message":          "string",    //信息
    "followings": [
        {
            user_id:    integer      //元素是int的用户id
        }
    ]
}
```

**返回示例**

- 200
```
{
    "code": 200,
    "message": "OK",
    "followings": [
        {
            user_id: 5    
        }
        {
            user_id: 12    
        }
        ...
    ]
}
```
- 400
```
    "code": 400,
    "message": "服务器发生错误"
```

- 401

```
    "code": 401,
    "message": "用户未登录"
```



## 获取当前用户的粉丝列表
> `GET /user/fans`

**参数**
```
无
```

**返回值**
```
{
    "code":             integer,     //状态码
    "message":          "string",    //信息
    "fans": [
        {
            user_id:    integer      //元素是int的用户id
        }
    ]
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK",
    "fans": [
        {
            user_id: 5    
        }
        {
            user_id: 12    
        }
        ...
    ]
}
```
- 400
```
    "code": 400,
    "message": "服务器发生错误"
```

- 401

```
    "code": 401,
    "message": "用户未登录"
```



# 任务

## 获取任务大厅的任务列表
> `GET /task`

**参数**

```
{
    "type":    integer    //0为最新任务, 1关注的人发布的任务, 2为价格降序
}
```

**返回值**

```
{
    "code":       integer,     //状态码
    "message":    "string",    //信息
    "tasks": [    
        {
            "task_id":            integer,     //订单ID(主键)
            "user_id":            integer,     //发布者id	
            "task_type":          "string",    //订单类型，0为拿快递和外卖，1为问卷
            "task_sketch":        "string",    //任务简介
            "task_bonus":         integer,     //悬赏金额
            "task_publishDate"    "string"     //发布时间
        }
    ]
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK",
    "tasks": [
        {
            //省略...
        }
    ]
}
```
- 400
```
    "code": 400,
    "message": "服务器发生错误"
```

- 401

```
    "code": 401,
    "message": "用户未登录"
```


## 根据任务id获取拿快递和外卖的详细信息

> `GET /task/delivery/detail`

**参数**

```
{
    "task_id":    integer
}
```

**返回值**

```
{
    "code":                    integer,     //状态码
    "message":                 "string",    //信息
    "delivery_detail":         "string",    //订单类型，0为拿快递和外卖，1为问卷
    "delivery_picked":         "string",    //任务简介
    "delivery_complished":     integer,     //悬赏金额
    "delivery_complishDate"    "string"     //发布时间
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK",
    "tasks": [
        {
            //省略...
        }
    ]
}
```
- 400
```
    "code": 400,
    "message": "服务器发生错误"
```

- 401

```
    "code": 401,
    "message": "用户未登录"
```


## 根据任务id获取问卷的详细信息

> `GET /task/questionnaire/detail`

**参数**

```
{
    "task_id":    integer
}
```

**返回值**

```
{
    "code":                      integer,     //状态码
    "message":                   "string",    //信息
    “questionnaire_id":          integer,     //问卷id
    "questionnaire_closed":      integer,     //是否截止
    "questionnaire_deadline":    string       //截止时间
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK",
    "tasks": [
        {
            //省略...
        }
    ]
}
```
- 400
```
    "code": 400,
    "message": "服务器发生错误"
```

- 401

```
    "code": 401,
    "message": "用户未登录"
```


## 根据问卷id获取问卷的所有题目的详细信息

> `GET /task/questionnaire/questions`

**参数**

```
{
    "questionnaire_id":    integer
}
```

**返回值**

```
{
    "code":                    integer,     //状态码
    "message":                 "string",    //信息
    "question_description":    "string",    //题目描述
    "question_type":           integer,     //题目类型，0为单选，1为多选，2为填空题
    "question_a":              "string",    //选项A描述
    "question_b":              "string",    //选项B描述
    "question_c":              "string",    //选项C描述
    "question_d":              "string"     //选项D描述
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK",
    "tasks": [
        {
            //省略...
        }
    ]
}
```
- 400
```
    "code": 400,
    "message": "服务器发生错误"
```

- 401

```
    "code": 401,
    "message": "用户未登录"
```


## 接受任务

> `POST /task/acceptance`

**参数**

```
{
    "task_id":    int    //订单ID(主键)
}
```

**返回值**

```
{
    "code":       integer,     //状态码
    "message":    "string",    //信息
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK"
}
```
- 400
```
    "code": 400,
    "message": "服务器发生错误"
```

- 401

```
    "code": 401,
    "message": "用户未登录"
```



## 完成任务

> `POST /task/complishment` 

**参数**

```
{
    "task_id":    int    //订单ID(主键)
}
```

**返回值**

```
{
    "code":       integer,     //状态码
    "message":    "string",    //信息
}
```

**返回示例**

- 200

```
{
    "code": 200,
    "message": "OK"
}
```

- 400

```
    "code": 400,
    "message": "服务器发生错误"
```

- 401

```
    "code": 401,
    "message": "用户未登录"
```





## 取消发布任务

> `DELETE /task` 

**参数**

```
{
    "task_id":    int    //订单ID(主键)
}
```

**返回值**
```
{
    "code":       integer,     //状态码
    "message":    "string",    //信息
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK"
}
```
- 400
```
    "code": 400,
    "message": "服务器发生错误"
```

- 401

```
    "code": 401,
    "message": "用户未登录"
```



## 新建任务

> `POST /task` 

**参数**

```
{
    "task_type":           "string",    //订单类型，0为拿快递和外卖，1为问卷
    "task_sketch":         "string"     //任务简述
    "task_bonus":          integer,     //悬赏金额
    "task_publishDate":    "string",    //发布时间  
}
```

**返回值**

```
{
    "code":       integer,     //状态码
    "message":    "string"     //信息
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK"
}
```
- 400
```
    "code": 400,
    "message": "服务器发生错误"
```


## 新建一个拿快递和外卖的任务

> `POST /task/delivery` 

**参数**

```
{
    "delivery_detail":          "string",    //订单类型，0为拿快递和外卖，1为问卷
    "delivery_picked":          "string"     //任务简述
    "delivery_complished":      integer,     //悬赏金额
    "delivery_complishDate":    "string"     //发布时间  
}
```

**返回值**

```
{
    "code":       integer,     //状态码
    "message":    "string"     //信息
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK"
}
```
- 400
```
    "code": 400,
    "message": "服务器发生错误"
```


## 新建一个问卷任务

> `POST /task/questionnaire` 

**参数**

```

```

**返回值**

```
{
    "code":       integer,     //状态码
    "message":    "string"     //信息
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK"
}
```
- 400
```
    "code": 400,
    "message": "服务器发生错误"
```


# 账单

## 新增当前用户的交易记录

> `POST /bill`

**参数**

```
{
    "bill_type":            integer,    //0为收入，1为支出
    "bill_number":          integer,    //账单金额
    "bill_description":     string,     //账单描述
    "bill_time":            string,     //账单时间
}
```

**返回值**

```
{
    "code":       integer,     //状态码
    "message":    "string"     //信息
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK"
}
```
- 400
```
    "code": 400,
    "message": "服务器发生错误"
```

- 401

```
    "code": 401,
    "message": "用户未登录"
```


## 获取当前用户的交易历史

> `GET /bill`

**参数**

```
无
```

**返回值**

```
{
    "code":            integer,     //状态码
    "message":         "string",    //信息
    "bills": [
        {
            "bill_type":            integer,    //0为收入，1为支出
            "bill_number":          integer,    //账单金额
            "bill_description":     string,     //账单描述
            "bill_time":            string,     //账单时间
        }
    ]
}
```

**返回示例**
- 200
```
{
    "code": 200,
    "message": "OK",
    "bills": [
        {
            //省略...
        }
    ]
}
```
- 400
```
    "code": 400,
    "message": "服务器发生错误"
```

- 401

```
    "code": 401,
    "message": "用户未登录"
```



## 当前用户的闲余币充值

> `暂未开放`


