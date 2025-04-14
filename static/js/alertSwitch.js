function alertSwitch(iconPar, titlePar, time = 3000) {

    const progressBarColors = {
        'info': '#3498db',
        'error': '#e04b4b',
        'success': '#198754'
    };

    const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: time,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.onmouseenter = Swal.stopTimer;
            toast.onmouseleave = Swal.resumeTimer;

            const progressBarColor = progressBarColors[iconPar];

            if (progressBarColor) {
                var progressBar = $('.swal2-timer-progress-bar');
                progressBar.css('background-color', progressBarColor);
            }
        }
    });

    Toast.fire({
        icon: iconPar,
        title: titlePar
    });
}