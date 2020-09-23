const toggleBtn = document.querySelector('.navbar__toggleBtn');
const menu = document.querySelector('.navbar__menu');
const icons = document.querySelector('.navbar__icons');

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