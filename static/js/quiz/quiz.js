const url1=window.location.href
const quizBox=document.getElementById('quiz-box')
const scoreBox=document.getElementById('score-box')
const resultBox=document.getElementById('result-box')
const timerBox=document.getElementById('timer-box')
const submitButton = document.getElementById('submit_btn')

let timer;

const activateTimer=(time)=>{
    if(time.toString().length < 2){

        timerBox.innerHTML=`<b>0${time}:00</b>`
    }else{
        timerBox.innerHTML=`<b>${time}:00</b>`
    }
    let minutes=time-1
    let seconds=60
    let displaySeconds
    let displayMinutes

    timer=setInterval(()=>{
        seconds --
        if(seconds < 0){
            seconds=59
            minutes --
        }if(minutes.toString().length < 2){
            displayMinutes='0'+minutes
        }else{
            displayMinutes = minutes}
        if(seconds.toString().length < 2){
            displaySeconds='0'+seconds
        }else{
            displaySeconds = seconds
        }
        if(minutes ===0 & seconds===0){
            timerBox.innerHTML=`<b>00:00</b>`
            setTimeout(()=>{
                clearInterval(timer)
                alert('Time Over')
                sendData()
            },500)
        }
        timerBox.innerHTML=`<b>${displayMinutes}:${displaySeconds}</b>`
    },1000)

}


$.ajax({
    type:'GET',
    url:`${url1}data`,
    success:function(response){
        data=response.data
        data.forEach(el =>{
            for (const [question,answers] of Object.entries(el)){
                quizBox.innerHTML +=`
                <hr>
                <div class="mb-4">
                <b>${question}</b>
                </div>
                `
            answers.forEach(answer=>{
                quizBox.innerHTML += `
                <div>
                <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                <label for="${question}">${answer}</label>
                </div>
                `
            })
            }
        });
        activateTimer(response.time)
    },
    error:function(error){
        console.log(error)
    }
})

const quizForm=document.getElementById('quiz-form')
const csrf=document.getElementsByName('csrfmiddlewaretoken')

const sendData=()=> {
    const elements=[...document.getElementsByClassName('ans')]
    const data={}
    data['csrfmiddlewaretoken']=csrf[0].value

    elements.forEach(el => {
        if(el.checked){
            data[el.name]=el.value
        } else{
            if(!data[el.name]){
                data[el.name]=null
            }
        }
    })
    
    // Clear the timer interval
    clearInterval(timer);

    // Set the timer value to "00:00"
    timerBox.innerHTML = '<b>00:00</b>';

    $.ajax({
        type:"POST",
        url:`${url1}save/`,
        data:data,
        success:function(response){
            const results=response.results
            // console.log(results)
            quizForm.classList.add('not-visible')
            document.getElementById('quiz-form').style.display = 'none';

            scoreBox.innerHTML = `${response.passed ? 'Congratulations!' : 'Ups..:('} Your result is ${response.score.toFixed(2)}`

            results.forEach(res=>{
                const resDiv=document.createElement("div")
                resDiv.classList.add('result-item');
                
                for (const [question, resp] of Object.entries(res)){
                    resDiv.innerHTML += question
                    const cls=['container','p-3','text-light','h3']
                    resDiv.classList.add(...cls)
                    if (resp=='not-answered'){
                        resDiv.innerHTML += '-not answered'
                        resDiv.classList.add('bg-danger')
                    }
                    else{
                        const answer=resp['answered']
                        const correct=resp['correct_answer']

                        if(answer==correct){
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML += `answered:${answer}`
                        }else{
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += ` | correct answer:${correct}`
                            resDiv.innerHTML += ` | answered:${answer} `
                        }
                    }
                }
                resultBox.append(resDiv)
            })
        },
        error:function(error){
            console.log(error)
        }
    })
}

submitButton.addEventListener('click', function (e) {
    e.preventDefault();
    sendData();
});