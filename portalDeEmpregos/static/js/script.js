function mostrarSection(sectionId) {
    const sections = document.querySelectorAll('main .section');
    sections.forEach(section => {
        section.classList.remove('active');
    });

    const activeSection = document.getElementById(sectionId);
    
    activeSection.classList.add('active');
    
}

function mostrarDiv(div_id) {
    const div = document.getElementById(div_id);

    if (div.style.display === 'none' || div.style.display === '') {
        div.style.display = 'block'; 
    } else {
        div.style.display = 'none';
    }

}

const buttons = document.querySelectorAll('.botao-menu');

function handleButtonClick(event) {
    buttons.forEach(button => button.classList.remove('active'));
    
    event.target.classList.add('active');
}

buttons.forEach(button => {
    button.addEventListener('click', handleButtonClick);
});


