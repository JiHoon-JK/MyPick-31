// 로딩하면 실행되는 함수 모음
// $(document).ready(function(){
//     //로그인을 했을 때
//     if({{session_nickname}} != ""){
//        $('.login').empty()
//        logout_html = '<a href="/" onclick="logout()">로그아웃</a>'
//        $('.login').html(logout_html)
//     }
//     else{
//
//     }
// })

// 메뉴바 함수를 위한 변수 선언
const toggleBtn = document.querySelector('.navbar_toggleBtn');
const menu = document.querySelector('.navbar_menu');
const icons = document.querySelector('.navbar_icons');

// 메뉴바를 누르면 메뉴 나오도록 하는 함수
toggleBtn.addEventListener('click', () => {
    menu.classList.toggle('active');
    icons.classList.toggle('active');
});


// detail html들을 초기화하는 함수
function new_detail() {
    console.log('하고있냐')
    $('.choco_detail').empty()
    $('.fruit_detail').empty()
    $('.nuts_detail').empty()
}

//버튼 애니메이션 실행 함수
function like_animation() {
    $('.like-button').toggleClass('is-active');
    alert('좋아요 기능은 회원가입을 해야 사용할 수 있습니다.')
}

// 로그인을 진행하면 나오는 html 체크 함수
function change_login_html(auth_id){

    var para = auth_id
    console.log(para);

    if(decodeNickname==true){
        receive_nickname = 
        login_html = `<div class="nickname">
        <a href="#" onclick="" id="user_nickname">${{user_nickname}}</a>
        </div>
        <div class="button">
        <a href="#" role="button" onclick="" id="Logout_button">Logout</a>
        <a href="#" role="button" onclick="" id="Mypage_button">MyPage</a>
        </div>`
        $('.user').append(login_html)
    }
    else{
        console.log('아무것도 없다.')
    }
}

//회원가입
function register() {
    auth_id = $('#new_inputEmail').val()
    nickname = $('#new_inputNickname').val()
    pw1 = $('#new_inputPassword1').val()
    pw2 = $('#new_inputPassword2').val()

    if (auth_id == "") {
        alert('이메일을 입력하세요');
        $('#new_inputEmail').focus();
        return;
    }

    let regEmail = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i;
    if ((regEmail.test($('#new_inputEmail').val()) == false)) {
        $('#new_inputEmail').val("이메일형식이 틀렸습니다.").css('color', 'red');
        $('#new_inputEmail').focus();
        return;
    }

    if (nickname == "") {
        alert('닉네임을 입력하세요');
        $('#new_inputNickname').focus();
        return;
    }

    if (pw1 == "") {
        alert('비밀번호를 입력하세요');
        $('#new_inputPassword1').focus();
        return;
    }

    if ($('#new_inputPassword1').val().length < 5) {
        alert('비밀번호는 다섯자리 이상으로 입력해주세요');
        $('#new_inputPassword1').focus();
        return;
    }

    if (pw1 != pw2) {
        alert('비밀번호가 일치하지 않습니다.');
    } else {
        $.ajax({
            type: "POST",
            url: "/customer_register",
            data: {
                auth_id: $('#new_inputEmail').val(),
                nickname: $('#new_inputNickname').val(),
                pwd: $('#new_inputPassword1').val()
            },
            success: function (response) {
                // 회원가입 성공
                if (response['result'] == 'success') {
                    alert('회원가입이 완료되었습니다.');
                    go_login_page();
                }
                // 이메일이 존재하는 경우
                else if (response['result'] == 'fail1') {
                    alert('이메일이 이미 존재합니다.');
                    $('#new_inputEmail').focus();
                }
                // 닉네임이 존재하는 경우
                else if (response['result'] == 'fail2') {
                    alert('닉네임이 이미 존재합니다.');
                    $('#new_inputNickname').focus();
                }
            }
        })
    }

}

// 로그인 함수
function login() {
    console.log('됐냐?')
    login_id = $('#new_inputEmail').val()
    login_pwd = $('#new_inputPassword').val()
    console.log(login_id)

    $.ajax({
        type: "POST",
        url: "/customer_login",
        data: {receive_id: login_id, receive_pwd: login_pwd},
        success: function (response) {
            // 로그인에 성공한 경우
            if (response['result'] == 'success') {
                user_nickname = response['userdb'];
                alert(user_nickname + '님! ' + 'MyPick31 에 오신 것을 환영합니다!');
                location.href = "/?nickname=" + user_nickname;
            }
            // 로그인에 실패한 경우 1 (비밃번호 틀림)
            else if (response['result'] == 'fail1') {
                alert('비밃번호가 다릅니다.');
                $('#new_inputPassword').focus();
            }
            // 로그인에 실패한 경우 2 (계정이 틀림)
            else if (response['result'] == 'fail2') {
                alert('계정이 존재하지 않습니다.');
                $('#new_inputEmail').focus();
            }
        }
    })
}

//로그아웃 함수
function logout(){
jbResult = confirm( "정말 로그아웃을 하시겠습니까?" );
if(jbResult == true){
  $.ajax({
   type: "POST",
   url: "/customer_logout",
   data: {},
   success: function(response){
    location.href="/"
  }
})
}
else{
}
}

//세션 받는 함수
function receive_session(){

}

//login 페이지로 이동하는 함수
function go_login_page() {
    location.href = "/login"
}

function check_spoon() {

    spoon_html = '<i class="fas fa-utensil-spoon"></i>'
    $('')

}

function choco_detail() {

    new_detail()

    choco_detail_html = '<i class="fas fa-angle-double-right"></i><li><a href="#"><span>다크초코</span></a></li><li><a href="#"><span>밀크초코</span></a></li><li><a href="#"><span>화이트초코</span></a></li>'
    $('.choco_detail').append(choco_detail_html)
}

function fruit_detail() {

    new_detail()

    fruit_detail_html = '<i class="fas fa-angle-double-right"></i><li><a href="#"><span>오렌지</span></a></li><li><a href="#"><span>자두</span></a></li><li><a href="#"><span>레몬</span></a></li>'
    $('.fruit_detail').append(fruit_detail_html)
}

function nuts_detail() {

    new_detail()

    nuts_detail_html = '<i class="fas fa-angle-double-right"></i><li><a href="#"><span>땅콩</span></a></li><li><a href="#"><span>호두</span></a></li>'
    $('.nuts_detail').append(nuts_detail_html)

}

// detail.html에서 사용
function review_save() {
    alert('리뷰를 저장했습니다!')

    ice_cream_name = $('.ice-cream_title').text()
    // print(ice_cream_name)
    // reviewer = "{{sessionemail}}"
    // print(reviewer)
    ice_cream_review = $('review_box').text()
    // print(ice_cream_review)

    // ajax로 서버에 보내야함
}

function createCB() {
    let cbase1 = $('#cbase1').val();
    let cbase2 = $('#cbase2').val();
    $.ajax({
        type: 'post',
        url: '/createCB',
        data: {
            'cbase1': cbase1,
            'cbase2': cbase2
        },
        success: function (response) {
            if (response["result"] == "success") {
                alert(response["msg"]);
                window.location.reload();
            } else {
                alert('서버 오류!')
            }
        }
    })
}

function createCT() {
    let ctopping1 = $('#ctopping1').val();
    let ctopping2 = $('#ctopping2').val();
    $.ajax({
        type: 'post',
        url: '/createCT',
        data: {
            'ctopping1': ctopping1,
            'ctopping2': ctopping2
        },
        success: function (response) {
            if (response["result"] == "success") {
                alert(response["msg"]);
                window.location.reload();
            } else {
                alert('서버 오류!')
            }
        }
    })
}

function createCS() {
    let csyrup1 = $('#csyrup1').val();
    let csyrup2 = $('#csyrup2').val();
    $.ajax({
        type: 'post',
        url: '/createCS',
        data: {
            'csyrup1': csyrup1,
            'csyrup2': csyrup2
        },
        success: function (response) {
            if (response["result"] == "success") {
                alert(response["msg"]);
                window.location.reload();
            } else {
                alert('서버 오류!')
            }
        }
    })
}

function createF_signature() {
    let name = $('#name_sg').val();
    let name_eng = $('#name_eng_sg').val();
    let base = $('#base_sg').val();
    let topping = $('#topping_sg').val();
    let syrup = $('#syrup_sg').val();
    let kcal = $('#kcal_sg').val();
    let allergens = $('#allergens_sg').val();
    let img = $('#img_sg').val();
    let heart = $('#heart_sg').val();
    $.ajax({
        type: 'post',
        url: '/createF_SG',
        data: {
            'name': name,
            'name_eng': name_eng,
            'base' : base,
            'topping' : topping,
            'syrup' : syrup,
            'kcal' : kcal,
            'allergens' : allergens,
            'img' : img,
            'heart' : heart
        },
        success: function (response) {
            if (response["result"] == "success") {
                alert(response["msg"]);
                window.location.reload();
            } else {
                alert('서버 오류!')
            }
        }
    })

}

function createF_season() {
    let name = $('#name_ss').val();
    let name_eng = $('#name_eng_ss').val();
    let base = $('#base_ss').val();
    let topping = $('#topping_ss').val();
    let syrup = $('#syrup_ss').val();
    let kcal = $('#kcal_ss').val();
    let allergens = $('#allergens_ss').val();
    let img = $('#img_ss').val();
    let heart = $('#heart_ss').val();
    $.ajax({
        type: 'post',
        url: '/createF_SS',
        data: {
            'name': name,
            'name_eng': name_eng,
            'base' : base,
            'topping' : topping,
            'syrup' : syrup,
            'kcal' : kcal,
            'allergens' : allergens,
            'img' : img,
            'heart' : heart
        },
        success: function (response) {
            if (response["result"] == "success") {
                alert(response["msg"]);
                window.location.reload();
            } else {
                alert('서버 오류!')
            }
        }
    })

}