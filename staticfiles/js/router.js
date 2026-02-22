document.addEventListener('DOMContentLoaded', () => {
    const handleRoute = () => {
        const hash = window.location.hash || '#home';
        const sections = document.querySelectorAll('.page-content');
        const navLinks = document.querySelectorAll('nav a');

        sections.forEach(section => {
            if (`#${section.id}` === hash) {
                section.classList.add('active');
                section.style.display = 'block';
            } else {
                section.classList.remove('active');
                section.style.display = 'none';
            }
        });

        // Atualizar estilo visual no menu
        navLinks.forEach(link => {
            link.classList.toggle('text-cyan-400', link.getAttribute('href') === hash);
        });

        // Scroll para o topo ao trocar de rota
        window.scrollTo(0, 0);
    };

    window.addEventListener('hashchange', handleRoute);
    handleRoute(); // Executa ao carregar
});