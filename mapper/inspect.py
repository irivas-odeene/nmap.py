def avisos(scan: Scan, reglas: dict[list[tuple[int|str], str, str]]):
    for host in scan.hosts:
        print(f"Analysis for {host.addresses[0].addr}")
        for regla, texto, tipo in reglas:
            badge = '043' if tipo == 'aviso' else '101'
            puertos = set()

            for puerto in regla:
                s = host.find(puerto)
                if s:
                    puertos.add(s)

            for puerto in puertos:
                print(f"\t\033[{badge}m {tipo.upper()} \033[0m {puerto.portnumber}/{puerto.protocol} ({puerto.service.name}) {texto}")
