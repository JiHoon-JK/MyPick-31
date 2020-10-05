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
function like_animation(){

	$('.like-button').toggleClass('is-active');
	alert('좋아요 기능은 회원가입을 해야 사용할 수 있습니다.')
};


//회원가입
function register(){
    auth_id = $('#new_inputEmail').val()
    nickname = $('#new_inputNickname').val()
    pw1 = $('#new_inputPassword1').val()
    pw2 = $('#new_inputPassword2').val()

    if(auth_id==""){
        alert('이메일을 입력하세요');
        $('#new_inputEmail').focus();
        return;
    }

    let regEmail = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i;
    if((regEmail.test($('#new_inputEmail').val())==false)){
        $('#new_inputEmail').val("이메일형식이 틀렸습니다.").css('color','red');
        $('#new_inputEmail').focus();
        return;
    }

    if(nickname==""){
        alert('닉네임을 입력하세요');
        $('#new_inputNickname').focus();
        return;
    }

    if(pw1==""){
        alert('비밀번호를 입력하세요');
        $('#new_inputPassword1').focus();
        return;
    }

    if($('#new_inputPassword1').val().length < 5){
        alert('비밀번호는 다섯자리 이상으로 입력해주세요');
        $('#new_inputPassword1').focus();
        return;
    }

    if(pw1 != pw2){
        alert('비밀번호가 일치하지 않습니다.');
    }
    else{
        $.ajax({
            type: "POST",
            url : "/customer_register",
            data : {auth_id:$('#new_inputEmail').val(),nickname:$('#new_inputNickname').val(), pwd:$('#new_inputPassword1').val()},
            success : function(response){
                // 회원가입 성공
                if(response['result'] == 'success'){
                    alert('회원가입이 완료되었습니다.');
                    go_login_page();
                }
                // 이메일이 존재하는 경우
                else if(response['result'] == 'fail1'){
                    alert('이메일이 이미 존재합니다.');
                    $('#new_inputEmail').focus();
                }
                // 닉네임이 존재하는 경우
                else if(response['result'] == 'fail2'){
                    alert('닉네임이 이미 존재합니다.');
                    $('#new_inputNickname').focus();
                }
            }
        })
    }

}

function login() {
    console.log('됐냐?')
    login_id = $('#new_inputEmail').val()
    login_pwd = $('#new_inputPassword').val()
    console.log(login_id)

    $.ajax({
        type: "POST",
        url: "/customer_login",
        data: {receive_id:login_id,receive_pwd:login_pwd},
        success: function(response){
            // 로그인에 성공한 경우
            if(response['result'] == 'success'){
                user_nickname = response['userdb'];
                alert(user_nickname+'님! '+'MyPick31 에 오신 것을 환영합니다!');
                go_index_page();
            }
            // 로그인에 실패한 경우 1 (비밃번호 틀림)
            else if(response['result'] == 'fail1'){
                alert('비밃번호가 다릅니다.');
                $('#new_inputPassword').focus();
            }
            // 로그인에 실패한 경우 2 (계정이 틀림)
            else if(response['result'] == 'fail2'){
                alert('계정이 존재하지 않습니다.');
                $('#new_inputEmail').focus();
            }
        }
    })
}

function go_login_page() {
    location.href = "/login"
}

function go_index_page() {
    location.href= "/"
}

function check_spoon() {
	
	spoon_html = '<i class="fas fa-utensil-spoon"></i>'
	$('')

}

function choco_detail(){

	new_detail()

	choco_detail_html = '<i class="fas fa-angle-double-right"></i><li><a href="#"><span>다크초코</span></a></li><li><a href="#"><span>밀크초코</span></a></li><li><a href="#"><span>화이트초코</span></a></li>'
	$('.choco_detail').append(choco_detail_html)
}

function fruit_detail(){

	new_detail()

	fruit_detail_html = '<i class="fas fa-angle-double-right"></i><li><a href="#"><span>오렌지</span></a></li><li><a href="#"><span>자두</span></a></li><li><a href="#"><span>레몬</span></a></li>'
	$('.fruit_detail').append(fruit_detail_html)
}

function nuts_detail(){

	new_detail()

	nuts_detail_html = '<i class="fas fa-angle-double-right"></i><li><a href="#"><span>땅콩</span></a></li><li><a href="#"><span>호두</span></a></li>'
	$('.nuts_detail').append(nuts_detail_html)
	
}

// detail.html에서 사용
function review_save(){
	alert('리뷰를 저장했습니다!')
	
	ice_cream_name = $('.ice-cream_title').text()
	// print(ice_cream_name)
	// reviewer = "{{sessionemail}}"
	// print(reviewer)
	ice_cream_review = $('review_box').text()
	// print(ice_cream_review)

	// ajax로 서버에 보내야함
}