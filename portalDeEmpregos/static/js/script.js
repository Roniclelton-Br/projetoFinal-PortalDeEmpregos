function mostrarSection(sectionId) {
    const sections = document.querySelectorAll('main .section');
    sections.forEach(section => {
        section.classList.remove('active');
    });

    const activeSection = document.getElementById(sectionId);
    
    activeSection.classList.add('active');
    
}



const buttons = document.querySelectorAll('.botao-menu');

function handleButtonClick(event) {
    buttons.forEach(button => button.classList.remove('active'));
    
    event.target.classList.add('active');
}

buttons.forEach(button => {
    button.addEventListener('click', handleButtonClick);
});
