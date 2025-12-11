() => {
        const selectors = [
            'button', 
            'a', 
            'input', 
            'select', 
            'textarea',
            '[role="button"]',
            '[onclick]'
        ];
        
        const elements = document.querySelectorAll(selectors.join(','));
        
        const results = [];
        let counter = 1;

        elements.forEach((el) => {
            const rect = el.getBoundingClientRect();
            const style = window.getComputedStyle(el);
            if (rect.width < 5 || rect.height < 5 || style.visibility === 'hidden' || style.opacity === '0') {
                return;
            }

            if (rect.bottom < 0 || rect.top > window.innerHeight || rect.right < 0 || rect.left > window.innerWidth) {
                return;
            }

            results.push({
                id: counter++,
                tagName: el.tagName.toLowerCase(),
                text: el.innerText.slice(0, 50).replace(/\n/g, ' '),
                rect: {
                    x: rect.x,
                    y: rect.y,
                    width: rect.width,
                    height: rect.height
                }
            });
        });

        return results;
    }