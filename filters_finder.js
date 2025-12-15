() => {
    function findByText(keyword) {
        const xpath = `//*[self::button or self::div or self::span][contains(text(), '${keyword}')]`;
        const result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
        
        for (let i = 0; i < result.snapshotLength; i++) {
            const el = result.snapshotItem(i);
            const rect = el.getBoundingClientRect();
            
            if (rect.width > 0 && rect.height > 0 && rect.width < 500) {
                return {
                    found: true,
                    text: keyword,
                    rect: {
                        x: rect.x,
                        y: rect.y,
                        width: rect.width,
                        height: rect.height
                    }
                };
            }
        }
        return { found: false, text: keyword };
    }

    const targets = [
        // "Filter",           // The main toggle button (if mobile/collapsed)
        "Location",         // Location Dropdown
        "Class Type",      // Class Type Dropdown
        "Instructor"   // Instructor Dropdown
    ];

    return targets.map(label => findByText(label));
}