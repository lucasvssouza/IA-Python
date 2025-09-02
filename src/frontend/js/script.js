$(document).ready(function () {
    const emailFileInput = $('#email-file');
    const emailTextInput = $('#email-text');
    const clearFileBtn = $('#clear-file-btn');
    const themeToggler = $('#theme-toggler');
    const themeIcon = themeToggler.find('i');
    const htmlElement = $('html');
    const resultsContainer = $('#results-container')
    const suggestedReply = $('#suggested-reply');

    // --- SCRIPT DE TEMA ---
    const setTheme = (theme) => {
        htmlElement.attr('data-bs-theme', theme);
        if (theme === 'dark') {
            themeIcon.removeClass('bi-moon-stars-fill').addClass('bi-sun-fill');
        } else {
            themeIcon.removeClass('bi-sun-fill').addClass('bi-moon-stars-fill');
        }
        localStorage.setItem('theme', theme);
    };

    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);

    themeToggler.on('click', function () {
        const currentTheme = htmlElement.attr('data-bs-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
    });
    // --- SCRIPT DE TEMA ---

    // --- VERIFICAÇÃO DO TIPO DE ARQUIVO ---
    emailFileInput.on('change', function () {
        const file = this.files[0];
        if (file) {
            const allowedExtensions = /(\.txt|\.pdf)$/i;

            if (!allowedExtensions.exec(file.name)) {
                Swal.fire({
                    icon: 'error',
                    title: 'Tipo de Arquivo Inválido',
                    text: 'Por favor, selecione apenas arquivos .txt ou .pdf.',
                });

                $(this).val('');
                return false;
            }
        }
    });
    // --- VERIFICAÇÃO DO TIPO DE ARQUIVO ---

    // --- EXCLUSIVIDADE DOS INPUTS ---
    emailFileInput.on('change', function () {
        if (this.files.length > 0) {
            clearFileBtn.removeClass('d-none');
            emailTextInput.val('');
        }

    });

    emailTextInput.on('input', function () {
        if ($(this).val().trim() !== '' && emailFileInput.val() !== '') {
            emailFileInput.val('');
            clearFileBtn.addClass('d-none');
        }
    });
    // --- EXCLUSIVIDADE DOS INPUTS ---

    // --- BOTÃO DE LIMPAR ARQUIVO ---
    clearFileBtn.on('click', function () {
        emailFileInput.val('');
        $(this).addClass('d-none');
    });
    // --- BOTÃO DE LIMPAR ARQUIVO ---

    // --- ENVIO DE FORMULÁRIO ---
    $('#email-form').on('submit', function (event) {
        event.preventDefault();
        const textValue = $('#email-text').val();
        const fileValue = $('#email-file')[0].files[0];

        if (!textValue && !fileValue) {
            Swal.fire({
                icon: 'warning',
                title: 'Atenção',
                text: 'Por favor, insira um texto ou envie um arquivo.',
            });
            return;
        }

        const formData = new FormData();
        if (textValue) {
            formData.append('email_text', textValue);
        } else if (fileValue) {
            formData.append('email_file', fileValue);
        }

        resultsContainer.addClass('d-none');

        Swal.fire({
            title: 'Analisando e-mail...',
            text: 'Aguarde um momento, a IA está trabalhando.',
            allowOutsideClick: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        $.ajax({
            url: '/verificar-email',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (data) {
                Swal.close();

                if (data.status === 'sucesso' && data.resultado) {
                    const classe = data.resultado.classe;
                    const classification = classe === 2 ? 'Produtivo' : 'Improdutivo';
                    const colors = ["bg-danger", "bg-success"]
                    $('#classification-result').text(classification);
                    $('#classification-badge').removeClass().addClass("rounded p-2 fs-6 " + colors[classe - 1]);
                    suggestedReply.empty();

                    const textResult = (data.resultado.texto.split("\n"));

                    textResult.forEach(element => {
                        var mb = 2;
                        if (element.trim() == "") {
                            mb = 4;
                        }
                        console.log(element.trim() == "");
                        const paragraphHTML = `<p class="mb-${mb}">${element}</p>`;
                        suggestedReply.append(paragraphHTML);
                    });

                    resultsContainer.removeClass('d-none');
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Erro no Processamento',
                        text: data.mensagem || 'Ocorreu um erro inesperado.',
                    });
                }
            },
            error: function (jqXHR) {
                const errorMessage = jqXHR.responseJSON ? jqXHR.responseJSON.detail : 'Falha na comunicação com o servidor.';

                Swal.fire({
                    icon: 'error',
                    title: 'Oops... Algo deu errado!',
                    text: errorMessage,
                });
            }
        });
    });
    // --- ENVIO DE FORMULÁRIO ---
});