const tabs = document.querySelectorAll('.pack-tab__btns>.btn');
const all_content = document.querySelectorAll('.pack-content');
console.log(tabs)
tabs.forEach((tab, index) => {
    tab.addEventListener('click', (e)=>{
        tabs.forEach(tab=>{tab.classList.remove('active')})
        tab.classList.add('active');

        all_content.forEach(content=>{content.classList.remove('active')});
    all_content[index].classList.add('active');
    })

    
})


const tabs2 = document.querySelectorAll('.pack-tab__property-btns>.btn');
const all_content2 = document.querySelectorAll('.property-content');
console.log(tabs2)
tabs2.forEach((tab, index) => {
    tab.addEventListener('click', (e)=>{
        tabs2.forEach(tab=>{tab.classList.remove('active')})
        tab.classList.add('active');

        all_content2.forEach(content=>{content.classList.remove('active')});
    all_content2[index].classList.add('active');
    })

    
})