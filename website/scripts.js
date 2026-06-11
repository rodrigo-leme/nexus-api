/**
 * Space Code LTDA — Site Institucional
 * Global Solution 2026 (Sistemas Operacionais)
 *
 * Funcionalidades:
 * 1. Formulario de contato -> salva em JSON (localStorage + download)
 * 2. Navbar scroll effect
 * 3. Smooth scroll
 */

// ============================================================
// ARMAZENAMENTO DE CONTATOS
// ============================================================

/**
 * Carrega contatos existentes do localStorage.
 * Em ambiente IIS real, isso faria um POST para o backend.
 */
function getContatos() {
    try {
        var data = localStorage.getItem('spacecode_contatos');
        return data ? JSON.parse(data) : [];
    } catch (e) {
        return [];
    }
}

/**
 * Salva um novo contato no localStorage e gera o arquivo JSON.
 */
function salvarContato(contato) {
    var contatos = getContatos();
    contatos.push(contato);
    localStorage.setItem('spacecode_contatos', JSON.stringify(contatos));
    return contatos;
}

/**
 * Gera e faz download do arquivo contatos.json
 */
function downloadJSON(contatos) {
    var jsonStr = JSON.stringify(contatos, null, 2);
    var blob = new Blob([jsonStr], { type: 'application/json' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'contatos.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// ============================================================
// HANDLER DO FORMULARIO
// ============================================================

function handleSubmit(event) {
    event.preventDefault();

    var nome = document.getElementById('nome').value.trim();
    var sobrenome = document.getElementById('sobrenome').value.trim();
    var mensagem = document.getElementById('mensagem').value.trim();

    // Validacao obrigatoria
    if (!nome || !sobrenome || !mensagem) {
        alert('Por favor, preencha todos os campos obrigatorios.');
        return false;
    }

    var contato = {
        nome: nome,
        sobrenome: sobrenome,
        mensagem: mensagem,
        data: new Date().toISOString()
    };

    // Salva e gera JSON
    var todosContatos = salvarContato(contato);

    // Faz download automatico do arquivo JSON
    downloadJSON(todosContatos);

    // Feedback visual
    document.getElementById('contactForm').style.display = 'none';
    document.getElementById('formSuccess').style.display = 'block';

    // Log para demonstracao
    console.log('=== CONTATO SALVO ===');
    console.log(JSON.stringify(contato, null, 2));
    console.log('Total de contatos:', todosContatos.length);
    console.log('Arquivo contatos.json gerado para download.');

    return false;
}

// ============================================================
// NAVBAR SCROLL EFFECT
// ============================================================

window.addEventListener('scroll', function() {
    var navbar = document.getElementById('navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(10,22,40,0.98)';
        navbar.style.boxShadow = '0 4px 20px rgba(0,0,0,0.3)';
    } else {
        navbar.style.background = 'rgba(10,22,40,0.92)';
        navbar.style.boxShadow = 'none';
    }
});

// ============================================================
// SMOOTH SCROLL PARA LINKS INTERNOS
// ============================================================

document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        var target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});
