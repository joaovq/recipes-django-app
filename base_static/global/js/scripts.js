function myScope() {
    const forms = document.querySelectorAll('.form-delete')
    
    for(const form of forms) {
        if(form) {
            form.addEventListener("submit",(e) => {
                e.preventDefault()
    
                const confirmed = confirm('Are you sure?')
    
                if(confirmed) {
                    form.submit()
                }
            })
        }
    }
}

myScope()