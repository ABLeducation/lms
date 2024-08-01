const modalBtns=[...document.getElementsByClassName('modal-button')]
const modalBody=document.getElementById('modal-body-confirm')
const startBtn=document.getElementById('start-button')

const url=window.location.href

modalBtns.forEach(modalBtn=>modalBtn.addEventListener('click', ()=>{
    const pk=modalBtn.getAttribute('data-pk')
    const name=modalBtn.getAttribute('data-quiz')
    const numQuestions=modalBtn.getAttribute('data-questions')
    const scoretopass=modalBtn.getAttribute('data-pass')
    const time=modalBtn.getAttribute('data-time')

    modalBody.innerHTML=`
    <div class="h5">Are you sure you want to begin with <b>${name}</b>?</div>
    <div class="text-muted">
            <ul>
                <li>Topic Name:<b>${name}</b></li>
                <li>Number of Questions:<b>${numQuestions}</b></li>
                <li>Passing marks:<b>${scoretopass}</b></li>
                <li>Time Duration:<b>${time}</b></li>
            </ul>
    </div>
    `
    startBtn.addEventListener('click', ()=> {
        window.location.href=url+pk
    })
}))