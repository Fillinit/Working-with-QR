const tabs = document.querySelectorAll('.mark-btns>.mark-btn');
const all_content = document.querySelectorAll('.mark-content');
console.log(tabs)
tabs.forEach((tab, index) => {
    tab.addEventListener('click', (e)=>{
        tabs.forEach(tab=>{tab.classList.remove('active')})
        tab.classList.add('active');

        all_content.forEach(content=>{content.classList.remove('active')});
    all_content[index].classList.add('active');
    })  
})

// Tables 
const headingsMarkCode = document.querySelectorAll('.mark-code .orders-table__item-head');
const iconMarkCode = document.querySelectorAll('.mark-code .print-icon')
headingsMarkCode.forEach((heading, index) => {
    heading.addEventListener('click', (e)=>{
        headingsMarkCode.forEach(heading=>{heading.classList.remove('active')})
        heading.classList.add('active');
        iconMarkCode.forEach(content=>{content.classList.remove('active')});
        iconMarkCode[index].classList.add('active');
    })
})